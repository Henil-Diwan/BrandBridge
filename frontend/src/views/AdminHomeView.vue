<script setup>
import { ref, onMounted, nextTick } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import AdminHeader from "@/components/AdminHeader.vue";
import Chart from "chart.js/auto";

let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});

let Labels_Sponsors = ref([]);
let Values_Sponsors = ref([]);
let Values_Influencers = ref([]);
let Labels_Campaigns = ref([]);
let Values_Campaigns = ref([]);
let NonFlagged_Values = ref([]);
let Flagged_Values = ref([]);

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

    console.log(current_user.value);

    const response2 = await axios.get("http://127.0.0.1:5001/admin_home", {
      params: {}, // Pass user_id as a query parameter
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    Labels_Sponsors.value = response2.data.Labels_Sponsors;
    Labels_Campaigns.value = response2.data.Labels_Campaigns;
    Values_Campaigns.value = response2.data.Values_Campaign;
    Values_Sponsors.value = response2.data.Values_Sponsors;
    Values_Influencers.value = response2.data.Values_Influencers;
    NonFlagged_Values.value = response2.data.NonFlagged_Values;
    Flagged_Values.value = response2.data.Flagged_Values;

    nextTick(() => {
      const ctx = document.getElementById("myChart");
      new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: Labels_Sponsors.value,
          datasets: [
            {
              data: Values_Sponsors.value,
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Distribution of Sponsors",
            },
          },
        },
      });

      const ctx2 = document.getElementById("influencerChart");
      new Chart(ctx2, {
        type: "doughnut",
        data: {
          labels: Labels_Sponsors.value,
          datasets: [
            {
              data: Values_Influencers.value,
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Distribution of Influencers",
            },
          },
        },
      });

      const ctx3 = document.getElementById("campaignChart");
      new Chart(ctx3, {
        type: "bar",
        data: {
          labels: Labels_Campaigns.value,
          datasets: [
            {
              data: Values_Campaigns.value,
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
          plugins: {
            title: {
              display: true,
              text: "Distribution of Campaigns",
            },
          },
        },
      });

      const ctx4 = document.getElementById("flaggedChart");
      new Chart(ctx4, {
        type: "bar",
        data: {
          labels: ["Campaigns", "Sponsors", "Influencers"],
          datasets: [
            {
              label: "Non Flagged",
              data: NonFlagged_Values.value,
              borderWidth: 1,
            },
            {
              label: "Flagged",
              data: Flagged_Values.value,
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
          plugins: {
            title: {
              display: true,
              text: "Flagged Campaigns",
            },
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
    <AdminHeader />

    <h2>Welcome Admin</h2>

    <div class="row justify-content-between">
      <div class="mychart-container w-50">
        <canvas id="myChart"></canvas>
      </div>
      <div class="mychart-container w-50">
        <canvas id="influencerChart"></canvas>
      </div>
    </div>
    <div class="row justify-content-between">
      <div class="mychart-container-2">
        <canvas id="campaignChart"></canvas>
      </div>
    </div>
    <div class="row mt-5 justify-content-between">
      <div class="mychart-container-2">
        <canvas id="flaggedChart"></canvas>
      </div>
    </div>
  </main>
</template>
