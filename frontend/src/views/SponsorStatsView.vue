<script setup>
import { ref, onMounted, nextTick } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import SponsorHeader from "@/components/SponsorHeader.vue";
import SponsorFooter from "@/components/SponsorFooter.vue";
import "vue3-toastify/dist/index.css";
import Chart from "chart.js/auto";
let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});
let current_sponsor = ref({
  id: -1,
  name: "",
  budget: 0,
  industry: "",
  flag: "",
  created_at: "",
});
let payment_labels = ref([]);
let payment_values = ref([]);
let status_values = ref([]);
let flagged_values = ref([]);
onMounted(async () => {
  try {
    document.title = `BrandBridge | Stats`;
    const token = JSON.parse(localStorage.getItem("user"))?.access_token;
    console.log(token);
    if (!token) {
      throw new Error("No token found");
    }
    const response = await axios.get("http://127.0.0.1:5001/protected", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    current_user.value = response.data.logged_in_as;
    current_sponsor.value = response.data.current_sponsor;
    const response2 = await axios.get("http://127.0.0.1:5001/sponsor_stats", {
      params: { sponsor_id: current_sponsor.value.id },
    });
    console.log(response2);
    payment_labels.value = response2.data.payment_labels;
    payment_values.value = response2.data.payment_values;
    flagged_values.value = response2.data.flagged_values;
    status_values.value = response2.data.status_values;
    nextTick(() => {
      const ctx = document.getElementById("payChart");
      if (ctx) {
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: payment_labels.value,
            datasets: [
              {
                data: payment_values.value,
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            scales: {
              y: { beginAtZero: true },
            },
            plugins: {
              title: {
                display: true,
                text: "Payment Distribution of Campaigns",
              },
            },
          },
        });
      }
      const ctx2 = document.getElementById("statusChart");
      new Chart(ctx2, {
        type: "doughnut",
        data: {
          labels: [
            "Open",
            "Requested By Influencer",
            "Requested To Influencer",
            "Accepted",
          ],
          datasets: [
            {
              data: status_values.value,
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "top" },
            title: { display: true, text: "Status of Campaigns" },
          },
        },
      });
      const ctx3 = document.getElementById("flaggedChart");
      new Chart(ctx3, {
        type: "doughnut",
        data: {
          labels: ["Unflagged", "Flagged"],
          datasets: [
            {
              data: flagged_values.value,
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "top" },
            title: { display: true, text: "Flagged Campaigns" },
          },
        },
      });
    });
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
</script>
<template>
  <main>
    <SponsorHeader />
    <div class="container">
      <div class="my-5 text-white">
        <h3>Stats</h3>
      </div>
    </div>
    <div class="container chart-container">
      <div class="row justify-content-between">
        <div class="mychart-container-2">
          <canvas id="payChart"></canvas>
        </div>
      </div>
      <div class="row justify-content-between">
        <div class="mychart-container">
          <canvas id="statusChart"></canvas>
        </div>
        <div class="mychart-container">
          <canvas id="flaggedChart"></canvas>
        </div>
      </div>
    </div>
    <SponsorFooter />
  </main>
</template>
<style scoped>
.chart-container {
  background-color: white;
  border-radius: 50px;
  padding: 50px;
  box-shadow: 20px 20px 30px 1px rgba(0, 0, 0, 0.2);
}
.mychart-container {
  width: 500px;
  height: 500px;
}
.mychart-container-2 {
  width: 100%;
}
</style>
