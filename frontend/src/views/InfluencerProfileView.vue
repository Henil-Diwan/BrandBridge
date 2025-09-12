<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import InfluencerHeader from "@/components/InfluencerHeader.vue";

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
let active_campaigns = ref([]);
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
    current_influencer.value = response.data.current_influencer;

    const response2 = await axios.get("http://127.0.0.1:5001/influencer_profile", {
      params: { influencer_id: current_influencer.value.id }, // Pass user_id as a query parameter
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    active_campaigns.value = response2.data.active;
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
    <InfluencerHeader />
    <h3 class="mt-5">Welcome {{ current_influencer.name }}</h3>

    <div class="row1">
        <div class="img-container float-end">
          <img
            :src="current_influencer.profile_pic ? `http://127.0.0.1:5001/uploads/${current_influencer.profile_pic}` : `http://127.0.0.1:5001/uploads/default.png`"
            height="200"
            alt="Profile Picture"
            class="rounded"
          />
        </div>
        <div class="details-container mb-5">
          <p class="mt-4">{{ current_influencer.about }}</p>
          <p>Category: {{ current_influencer.category }}</p>
          <p>Niche: {{ current_influencer.niche }}</p>
          <p>Reach: {{ current_influencer.reach }}</p>
          <p>Rating: {{ current_influencer.rating }}</p>
          <p>Views: {{ current_influencer.views }}</p>
          <RouterLink :to="'/update_influencer/'" class="btn btn-primary">Update Profile</RouterLink>
        </div>
      </div>

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
            <p class="font-italic text-muted">{{ campaign.desc }}</p>
            <div class="progress">
              <div
                class="progress-bar"
                :style="{ width: campaign.completion + '%' }"
              ></div>
            </div>
            <RouterLink :to="'/change_campaign/'+campaign.id" class="btn btn-primary my-3">change</RouterLink>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>You have no active campaigns at the moment.</p>
    </div>

      <div class="mt-5">
        <h5>Your Current Requests</h5>
        <div v-if="requested_campaigns.length === 0" class="">
          You're Up to Date!
        </div>
        <div v-else>
          <div v-for="campaign in requested_campaigns" :key="campaign.id" class="card">
            <div class="card-body">
              <h5 class="card-title">
                <RouterLink to="/" class="link link-dark">{{ campaign.name }}</RouterLink>
              </h5>
              <p class="card-text">By: {{ campaign.sponsor_name }}</p>
              <div class="card-body">
                <a @click.prevent="acceptCampaign(campaign.id)" class="btn btn-primary mx-2">Accept</a>
                <a @click.prevent="rejectCampaign(campaign.id)" class="btn btn-danger mx-2">Reject</a>
              </div>
            </div>
          </div>
        </div>
    </div>

    

  </main>
</template>
