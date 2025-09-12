<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import SponsorHeader from "@/components/SponsorHeader.vue";
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
      params: { sponsor_id: current_sponsor.value.id }, // Pass user_id as a query parameter
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

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
    const response_accept = await axios.post(`http://127.0.0.1:5001/accept_campaign/${campaignId}`);
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
    <h3 class="mt-5">Welcome {{ current_sponsor.name }}</h3>

    <h5>Your Current Campaigns</h5>
    <div v-if="active_campaigns.length > 0">
      <div class="container">
        <div
          v-for="campaign in active_campaigns"
          :key="campaign.id"
          class="card mb-5"
        >
          <div class="card-body">
            <h4>
                <RouterLink to="/">{{ campaign.name }}</RouterLink>
            </h4>
            <p class="font-italic text-muted">Status: {{ campaign.status }}</p>
            <div class="progress">
              <div
                class="progress-bar"
                :style="{ width: campaign.completion + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>You have no active campaigns at the moment.</p>
    </div>


    <h5>Your Current Requests</h5>
    <div v-if="requested_campaigns.length > 0">
      <div class="container">
        <div v-for="campaign in requested_campaigns" :key="campaign.id" class="row gap-5 justify-content-start">
          <div class="col-lg-3 col-md-8 mb-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">
                    <RouterLink to="/" class="link-dark">{{ campaign.name }}</RouterLink>
                </h5>
                <p class="card-text">
                  By: 
                  <RouterLink to="/" class="link-dark">{{ campaign.influencer_name }}</RouterLink>
                </p>
                <div class="card-body">
                  <button @click="acceptCampaign(campaign.id)" class="btn btn-primary">Accept</button>
                  <button @click="rejectCampaign(campaign.id)" class="btn btn-danger">Reject</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>You have no pending requests at the moment.</p>
    </div>



    <h5>Your Ended Campaigns</h5>
    <div v-if="ended_campaigns.length > 0">
      <div class="container">
        <div
          v-for="campaign in ended_campaigns"
          :key="campaign.id"
          class="card mb-5"
        >
          <div class="card-body">
            <h4>
                <RouterLink to="/">{{ campaign.name }}</RouterLink>
            </h4>
            <p class="font-italic text-muted">Status: {{ campaign.status }}</p>
            <div class="progress">
              <div
                class="progress-bar"
                :style="{ width: campaign.completion + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>You have no ended campaigns at the moment.</p>
    </div>

  </main>
</template>
