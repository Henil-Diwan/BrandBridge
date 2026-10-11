<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
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
let active_campaigns = ref([]);
let requested_campaigns = ref([]);
onMounted(async () => {
  try {
    document.title = `BrandBridge | Influencer Profile`;
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
      "http://127.0.0.1:5001/influencer_profile",
      {
        params: { influencer_id: current_influencer.value.id },
      }
    );
    console.log(response2);
    active_campaigns.value = response2.data.active;
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
    <InfluencerHeader />
    <div class="wrapper my-5">
      <div class="container d-flex justify-content-center">
        <div class="row1">
          <div class="img-container float-end">
            <img
              :src="
                current_influencer.profile_pic
                  ? `http://127.0.0.1:5001/uploads/${current_influencer.profile_pic}`
                  : `http://127.0.0.1:5001/uploads/default.png`
              "
              height="200"
              alt=""
              class="rounded"
            />
          </div>
          <div class="details-container mb-5">
            <h3>Welcome {{ current_influencer.name }}</h3>
            <p class="mt-4">{{ current_influencer.about }}</p>
            <p>Category: {{ current_influencer.category }}</p>
            <p>Niche: {{ current_influencer.niche }}</p>
            <p>Reach: {{ current_influencer.reach }}</p>
            <p>Rating: {{ current_influencer.rating }}</p>
            <p><i class="bi bi-eye-fill"></i> {{ current_influencer.views }}</p>
            <RouterLink :to="'/update_influencer/'" class="button button-blue"
              >Update Profile</RouterLink
            >
          </div>
          <div class="container">
            <div>
              <h5>Your Current Campaigns</h5>
            </div>
          </div>
          <div v-if="active_campaigns.length == 0" class="container">
            <div>
              <p class="h6">No Current Campaigns</p>
            </div>
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
                      :to="`/show_campaign/${campaign.id}`"
                      class="link-dark"
                      >{{ campaign.name }}</RouterLink
                    >
                  </h4>
                  <p class="font-italic text-muted">{{ campaign.desc }}</p>
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
                  <div class="change">
                    <RouterLink
                      :to="'/change_campaign/' + campaign.id"
                      class="button button-pink"
                      >change</RouterLink
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="container mt-5">
            <div>
              <h5>Your Current Requests</h5>
            </div>
          </div>
          <div v-if="requested_campaigns.length === 0" class="container">
            <div>
              <p class="h6">You're Up to Date!</p>
            </div>
          </div>
          <div
            v-else
            v-for="campaign in requested_campaigns"
            :key="campaign.id"
            class="card"
          >
            <div class="card-body">
              <h5 class="card-title">
                <RouterLink
                  :to="`/show_campaign/${campaign.id}`"
                  class="link link-dark"
                  >{{ campaign.name }}</RouterLink
                >
              </h5>
              <p class="card-text">By:{{ campaign.sponsor_name }}</p>
              <div class="card-body">
                <a
                  @click.prevent="acceptCampaign(campaign.id)"
                  class="button button-blue"
                  >Accept</a
                >
                <a
                  @click.prevent="rejectCampaign(campaign.id)"
                  class="button button-pink"
                  >Reject</a
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <InfluencerFooter />
  </main>
</template>
<style scoped>
.card-blue {
  border: 3px solid #5c9df1;
}
.card-pink {
  border: 3px solid #fa709a;
}
.card-purple {
  border: 3px solid #784ba8;
}
.bar-blue {
  background-color: #5c9df1;
}
.bar-pink {
  background-color: #fa709a;
}
.bar-purple {
  background-color: #784ba8;
}
.card {
  color: #40414a;
  font-weight: 500;
}
.back {
  text-align: center;
  font-size: small;
  margin-top: 25px;
}
h4 {
  font-size: large;
}
.ad_card {
  border: 2px solid #784ba887;
  border-radius: 10px;
  overflow: hidden;
  background: white;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.row1 {
  border-radius: 10px;
  background: white;
  width: 900px;
  padding: 20px;
  box-shadow: 20px 20px 30px 1px rgba(0, 0, 0, 0.2);
}
.button {
  text-decoration: none;
  border-radius: 5px;
  color: white;
  transition: 0.4s;
  margin-top: 35px;
  padding: 7px;
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
  color: white;
}
.comment-input {
  border: 2px solid #784ba887;
}
.change {
  margin-top: 25px;
}
@media only screen and (max-width: 550px) {
  .img-container {
    display: none;
  }
}
</style>
