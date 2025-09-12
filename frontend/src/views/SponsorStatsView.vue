<script setup>
import { ref, onMounted,nextTick } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import SponsorHeader from "@/components/SponsorHeader.vue";
import "vue3-toastify/dist/index.css";
import Chart from 'chart.js/auto';


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

    const response2 = await axios.get(
      "http://127.0.0.1:5001/sponsor_stats",
      {
        params: { sponsor_id: current_sponsor.value.id }, // Pass user_id as a query parameter
      }
    );

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    
      payment_labels.value=response2.data.payment_labels;
      payment_values.value=response2.data.payment_values;
      flagged_values.value=response2.data.flagged_values;
      status_values.value=response2.data.status_values;

       // Payment Distribution Bar Chart

       nextTick(() => {
      // Payment Distribution Bar Chart
      const ctx = document.getElementById("payChart");
      if (ctx) {
        new Chart(ctx, {
          type: 'bar',
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
              title: { display: true, text: 'Payment Distribution of Campaigns' },
            },
          },
        });
      }

      // Campaign Status Doughnut Chart
      const ctx2 = document.getElementById("statusChart");
        new Chart(ctx2, {
          type: 'doughnut',
          data: {
            labels: ['Open', 'Requested By Influencer', 'Requested To Influencer', 'Accepted'],
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
              legend: { position: 'top' },
              title: { display: true, text: 'Status of Campaigns' },
            },
          },
        });

      // Flagged Campaigns Doughnut Chart
        const ctx3 = document.getElementById("flaggedChart");
        new Chart(ctx3, {
          type: 'doughnut',
          data: {
            labels: ['Unflagged', 'Flagged'],
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
              legend: { position: 'top' },
              title: { display: true, text: 'Flagged Campaigns' },
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
    <h2>Stats for {{ current_sponsor.name }}</h2>

     <div v-if="payment_labels.length">
      <!-- Payment Distribution Chart -->
      <div class="mychart-container-2">
        <canvas id="payChart"></canvas>
      </div>

      <!-- Campaign Status Chart -->
      <div class="mychart-container w-50">
        <canvas id="statusChart"></canvas>
      </div>

      <!-- Flagged Campaigns Chart -->
      <div class="mychart-container w-50">
        <canvas id="flaggedChart"></canvas>
      </div>
    </div>


  </main>
</template>
