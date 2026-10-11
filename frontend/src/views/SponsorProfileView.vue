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
let active_campaigns = ref([]);
let ended_campaigns = ref([]);
let requested_campaigns = ref([]);
onMounted(async () => {
  try {
    document.title = `BrandBridge | Profile`;
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
    const response2 = await axios.get("http://127.0.0.1:5001/sponsor_profile", {
      params: { sponsor_id: current_sponsor.value.id },
    });
    console.log(response2);
    active_campaigns.value = response2.data.active;
    ended_campaigns.value = response2.data.prev;
    requested_campaigns.value = response2.data.requested;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
const acceptCampaign = async (campaignId) => {
  try {
    const response_accept = await axios.post(
      `http://127.0.0.1:5001/accept_campaign/${campaignId}`
    );
    toast("Campaign Accepted!", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.go();
      },
      autoClose: 1000,
    });
  } catch (err) {
    console.log(err);
    toast("An Error Occured", {
      theme: "auto",
      type: "error",
      dangerouslyHTMLString: true,
      autoClose: 1000,
    });
  }
};
const rejectCampaign = async (campaignId) => {
  try {
    const response_reject = await axios.post(
      `http://127.0.0.1:5001/reject_campaign/${campaignId}`
    );
    toast("Campaign Rejected!", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.go();
      },
      autoClose: 1000,
    });
  } catch (err) {
    console.log(err);
    toast("An Error Occured", {
      theme: "auto",
      type: "error",
      dangerouslyHTMLString: true,
      autoClose: 1000,
    });
  }
};
</script>
<template>
  <main>
    <SponsorHeader />
    <div class="container">
      <div class="my-5 text-white">
        <h3>Welcome {{ current_sponsor.name }}</h3>
      </div>
    </div>
    <div class="container">
      <div class="my-5 text-white">
        <h5>Your Current Campaigns</h5>
      </div>
    </div>
    <div v-if="active_campaigns.length == 0" class="my-5 text-white container">
      <h5>No Current Campaigns</h5>
    </div>
    <div v-else class="container">
      <div v-for="campaign in active_campaigns" :key="campaign.id">
        <div
          class="card mb-5 rounded"
          :class="{
            'card-blue': campaign.id % 3 === 1,
            'card-pink': campaign.id % 3 === 2,
            'card-purple': campaign.id % 3 === 0,
          }"
        >
          <div class="card-body p-5">
            <h4>
              <RouterLink
                class="link-dark"
                :to="`/show_campaign/${campaign.id}`"
                >{{ campaign.name }}</RouterLink
              >
            </h4>
            <p class="font-italic text-muted">Status: {{ campaign.status }}</p>
            <div class="container">
              <div class="progress" role="progressbar">
                <div
                  class="progress-bar"
                  :class="{
                    'bar-blue': campaign.id % 3 === 1,
                    'bar-pink': campaign.id % 3 === 2,
                    'bar-purple': campaign.id % 3 === 0,
                  }"
                  :style="{ width: campaign.completion + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="my-5 text-white">
        <h5>Your Current Requests</h5>
      </div>
    </div>
    <div v-if="requested_campaigns.length == 0" class="container">
      <div class="text-white">
        <p class="h6">You're Up to Date!</p>
      </div>
    </div>
    <div
      v-else
      v-for="campaign in requested_campaigns"
      :key="campaign.id"
      class="container"
    >
      <div class="row gap-5 justify-content-start">
        <div class="col-lg-3 col-md-8 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">
                <RouterLink
                  :to="`/show_campaign/${campaign.id}`"
                  class="link-dark"
                  >{{ campaign.name }}</RouterLink
                >
              </h5>
              <p class="card-text">
                By:
                <RouterLink
                  class="link-dark"
                  :to="`/view_influencer/${campaign.influencer}`"
                  >{{ campaign.influencer_name }}</RouterLink
                >
              </p>
              <div class="card-body text-center">
                <button
                  @click="acceptCampaign(campaign.id)"
                  class="button button-blue mx-3"
                >
                  Accept
                </button>
                <button
                  @click="rejectCampaign(campaign.id)"
                  class="button button-pink mx-3"
                >
                  Reject
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="my-5 text-white">
        <h5>Your Previous Campaigns</h5>
      </div>
    </div>
    <div v-if="ended_campaigns.length == 0" class="container">
      <div class="text-white">
        <p class="h6">No Previous Campaigns</p>
      </div>
    </div>
    <div v-else class="container">
      <div v-for="campaign in ended_campaigns" :key="campaign.id">
        <div
          class="card mb-5 rounded"
          :class="{
            'card-blue': campaign.id % 3 === 1,
            'card-pink': campaign.id % 3 === 2,
            'card-purple': campaign.id % 3 === 0,
          }"
        >
          <div class="card-body p-5">
            <h4>
              <RouterLink
                class="link-dark"
                :to="`/show_campaign/${campaign.id}`"
                >{{ campaign.name }}</RouterLink
              >
            </h4>
            <p class="font-italic text-muted">Status: {{ campaign.status }}</p>
            <div class="container">
              <div class="progress" role="progressbar">
                <div
                  class="progress-bar"
                  :class="{
                    'bar-blue': campaign.id % 3 === 1,
                    'bar-pink': campaign.id % 3 === 2,
                    'bar-purple': campaign.id % 3 === 0,
                  }"
                  :style="{ width: campaign.completion + '%' }"
                ></div>
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
.progress {
  height: 30px;
  border-radius: 20px;
}
.card-blue {
  border: 10px solid #5c9df1 !important;
}
.card-pink {
  border: 10px solid #fa709a !important;
}
.card-purple {
  border: 10px solid #784ba8 !important;
}
.bar-blue {
  background-color: #5c9df1 !important;
}
.bar-pink {
  background-color: #fa709a !important;
}
.bar-purple {
  background-color: #784ba8 !important;
}
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
</style>
