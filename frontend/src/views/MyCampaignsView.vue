<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import SponsorHeader from "@/components/SponsorHeader.vue";
import SponsorFooter from "@/components/SponsorFooter.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
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
let campaigns = ref([]);
let taskId = ref("");
onMounted(async () => {
  try {
    document.title = `BrandBridge | My Campaigns`;
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
    const response2 = await axios.get("http://127.0.0.1:5001/my_campaigns", {
      params: { user_id: current_user.value.user_id },
    });
    console.log(response2);
    campaigns.value = response2.data.campaigns;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
let deleteCampaign = async (campaignId) => {
  try {
    const delete_response = await axios.delete(
      `http://127.0.0.1:5001/delete_campaign/${campaignId}`
    );
    toast("Campaign Deleted Successfully", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.go();
      },
      autoClose: 1000,
    });
  } catch (error) {
    toast("An Error Occured", {
      theme: "auto",
      type: "error",
      dangerouslyHTMLString: true,
      autoClose: 1000,
    });
    console.log(error);
  }
};
let downloadCSV = async () => {
  const response = await fetch(
    `http://127.0.0.1:5001/download_csv/${current_sponsor.value.id}`
  );
  const data = await response.json();
  if (response.ok) {
    taskId.value = data["task_id"];
    const intv = setInterval(async () => {
      const csv_resp = await fetch(
        `http://127.0.0.1:5001/get_csv/${taskId.value}`
      );
      if (csv_resp.ok) {
        clearInterval(intv);
        window.location.href = `http://127.0.0.1:5001/get_csv/${taskId.value}`;
      }
    }, 100);
  }
};
</script>
<template>
  <main>
    <SponsorHeader />
    <div class="container">
      <div class="my-5 text-white">
        <h3>Your Campaigns</h3>
        <button
          class="button button-pink my-3 download_csv"
          @click="downloadCSV"
        >
          Download CSV
        </button>
      </div>
    </div>
    <div v-if="campaigns.length == 0" class="my-5 text-center text-white">
      <h5>No Current Campaigns</h5>
    </div>
    <div v-else class="container">
      <div class="container-2">
        <div class="row gap-5 justify-content-start">
          <div
            v-for="campaign in campaigns"
            :key="campaign.id"
            class="col-lg-3 col-md-8 mb-4 bg"
          >
            <div class="card" style="width: 100%">
              <div class="card-body">
                <h5 class="card-title">
                  <RouterLink
                    :to="`/show_campaign/${campaign.id}`"
                    class="link-dark"
                    >{{ campaign.name }}</RouterLink
                  >
                </h5>
                <p class="card-text">{{ campaign.desc }}</p>
              </div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  Preferred Category: {{ campaign.category }}
                </li>
                <li class="list-group-item">Goals: {{ campaign.goals }}</li>
                <li class="list-group-item">
                  Total Budget: {{ campaign.budget }}
                </li>
                <li class="list-group-item">
                  End Date: {{ campaign.end_date }}
                </li>
                <li class="list-group-item">
                  <i class="bi bi-eye-fill"></i> {{ campaign.views }}
                </li>
              </ul>
              <div
                v-if="campaign.status !== 'Accepted'"
                class="card-body text-center"
              >
                <router-link
                  :to="'/update/' + campaign.id"
                  class="button button-blue"
                  >Update</router-link
                >
                <button
                  @click="deleteCampaign(campaign.id)"
                  class="button button-pink"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <SponsorFooter />
  </main>
</template>
<style scoped>
.card {
  color: #40414a;
  font-weight: 500;
}
.button {
  text-decoration: none;
  border-radius: 5px;
  color: white;
  transition: 0.4s;
  margin-top: 35px;
  padding: 5px;
  border: none;
}
.button-pink {
  background: #fa709a;
}
.button-blue {
  background: #5c9df1;
}
.button:hover {
  background: #784ba8;
}
@media only screen and (min-width: 768px) {
  .download_csv {
    position: absolute;
    top: 0rem;
    right: 10rem;
  }
}
</style>
