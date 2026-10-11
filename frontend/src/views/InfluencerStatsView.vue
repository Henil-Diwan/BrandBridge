<script setup>
import { ref, onMounted, nextTick } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import "vue3-toastify/dist/index.css";
import Chart from "chart.js/auto";
import InfluencerHeader from "@/components/InfluencerHeader.vue";
import InfluencerFooter from "@/components/InfluencerFooter.vue";
let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});
let current_influencer = ref({
  id: -1,
  name: "",
  about: "",
  profile_pic: "",
  category: "",
  niche: "",
  reach: 0,
  views: 0,
  rating: 0.0,
  rating_no: 0,
  flag: "",
  created_at: "",
});
let payment_labels = ref([]);
let payment_values = ref([]);
let rating_values = ref([]);
let percent_complete = ref([]);
let percent_incomplete = ref([]);
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
    current_influencer.value = response.data.current_influencer;
    const response2 = await axios.get(
      "http://127.0.0.1:5001/influencer_stats",
      {
        params: { influencer_id: current_influencer.value.id },
      }
    );
    console.log(response2);
    payment_labels.value = response2.data.payment_labels;
    payment_values.value = response2.data.payment_values;
    rating_values.value = response2.data.rating_values;
    percent_complete.value = response2.data.percent_complete;
    percent_incomplete.value = response2.data.percent_incomplete;
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
      const ctx3 = document.getElementById("completeChart");
      console.log(payment_labels.value);
      if (ctx3) {
        new Chart(ctx3, {
          type: "bar",
          data: {
            labels: payment_labels.value,
            datasets: [
              {
                label: "Complete",
                data: percent_complete.value,
                borderWidth: 1,
              },
              {
                label: "Incomplete",
                data: percent_incomplete.value,
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
                text: "Completion Percent",
              },
            },
          },
        });
      }
      const ctx2 = document.getElementById("ratingChart");
      if (ctx2) {
        new Chart(ctx2, {
          type: "doughnut",
          data: {
            labels: ["0", "1", "2", "3", "4", "5"],
            datasets: [
              {
                data: rating_values.value,
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
              legend: {
                position: "top",
              },
              title: {
                display: true,
                text: "Influencer Ratings",
              },
            },
          },
        });
      }
    });
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
</script>
<template>
  <main>
    <InfluencerHeader />
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
      <div class="row justify-content-center">
        <div class="mychart-container-2">
          <canvas id="completeChart"></canvas>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="mychart-container">
          <canvas id="ratingChart"></canvas>
        </div>
      </div>
    </div>
    <InfluencerFooter />
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
