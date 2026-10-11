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
let influencers = ref([]);
let campaigns = ref([]);
let selectedCampaigns = ref([]);
let userCampaigns = ref([]);
let selectedInfluencerId = ref(null);
onMounted(async () => {
  try {
    document.title = `BrandBridge | Home`;
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
      "http://127.0.0.1:5001/sponsor_dashboard",
      {
        params: { user_id: current_user.value.user_id },
      }
    );
    console.log(response2);
    influencers.value = response2.data.influencers;
    campaigns.value = response2.data.campaigns;
    userCampaigns.value = response2.data.user_campaigns;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
const toggleCampaignSelection = (campaignId) => {
  if (selectedCampaigns.value.includes(campaignId)) {
    selectedCampaigns.value = selectedCampaigns.value.filter(
      (id) => id !== campaignId
    );
  } else {
    selectedCampaigns.value.push(campaignId);
  }
};
const submitRequest = async (infid) => {
  const requestdata = {
    campaign_ids: selectedCampaigns.value,
    influencer_id: selectedInfluencerId.value,
  };
  try {
    const response_update = await axios.post(
      "http://127.0.0.1:5001/request_to_influencer",
      requestdata,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );
    toast("Requets Sent Successfully", {
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
const openRequestModal = (influencerId) => {
  selectedInfluencerId.value = influencerId;
};
const generateStars = (rating) => {
  const filledStars = Math.floor(rating);
  const halfStar = rating % 1 >= 0.5 ? 1 : 0;
  const emptyStars = 5 - filledStars - halfStar;
  return {
    filledStars: Array(filledStars).fill("bi-star-fill"),
    halfStar: halfStar ? "bi-star-half" : null,
    emptyStars: Array(emptyStars).fill("bi-star"),
  };
};
</script>
<template>
  <body>
    <SponsorHeader />
    <div class="container">
      <div class="my-5 text-white">
        <h3>Top Voices in Your Industry</h3>
      </div>
    </div>
    <div v-if="influencers.length == 0" class="my-5 text-center text-white">
      <h5>No Current Influencers</h5>
    </div>
    <div v-else class="container">
      <div class="row gap-5 justify-content-start">
        <div
          v-for="influencer in influencers"
          :key="influencer.id"
          class="col-lg-3 col-md-8 mb-4 bg"
        >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">
                <RouterLink
                  class="link-dark"
                  :to="`/view_influencer/${influencer.id}`"
                  >{{ influencer.name }}</RouterLink
                >
              </h5>
              <p class="card-text">{{ influencer.about }}</p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                Category: {{ influencer.category }}
              </li>
              <li class="list-group-item">Niche: {{ influencer.niche }}</li>
              <li class="list-group-item">Reach: {{ influencer.reach }}</li>
              <li class="list-group-item">
                <i
                  v-for="(star, index) in generateStars(influencer.rating)
                    .filledStars"
                  :key="'filled-' + index"
                  class="bi"
                  :class="star"
                ></i>
                <i
                  v-if="generateStars(influencer.rating).halfStar"
                  class="bi"
                  :class="generateStars(influencer.rating).halfStar"
                ></i>
                <i
                  v-for="(star, index) in generateStars(influencer.rating)
                    .emptyStars"
                  :key="'empty-' + index"
                  class="bi"
                  :class="star"
                ></i>
              </li>
              <li class="list-group-item">
                <i class="bi bi-eye-fill"></i> {{ influencer.views }}
              </li>
            </ul>
            <div class="card-body text-center">
              <RouterLink
                :to="`/view_influencer/${influencer.id}`"
                class="button button-pink"
                >View Profile</RouterLink
              >
              <button
                type="button"
                class="button button-blue"
                @click="openRequestModal(influencer.id)"
                data-bs-toggle="modal"
                data-bs-target="#staticBackdrop"
              >
                Request
              </button>
              <RouterLink
                :to="`/rate/${influencer.id}`"
                class="button button-pink"
                >Rate</RouterLink
              >
            </div>
          </div>
        </div>
      </div>
      <div class="container">
        <div class="my-5 text-white">
          <h3>Current Campaigns in Your Industry</h3>
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
                  <p class="card-text">
                    {{ campaign.by }}
                  </p>
                  <h5 class="card-title">
                    <RouterLink
                      :to="`/show_campaign/${campaign.id}`"
                      class="link-dark"
                      >{{ campaign.name }}</RouterLink
                    >
                  </h5>
                  <p class="card-text">{{ campaign.desc }}...</p>
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
                    From: {{ campaign.start_date }} To: {{ campaign.end_date }}
                  </li>
                  <li class="list-group-item">
                    <i class="bi bi-eye-fill"></i> {{ campaign.views }}
                  </li>
                </ul>
                <div class="card-body text-center">
                  <RouterLink
                    :to="`/show_campaign/${campaign.id}`"
                    class="button button-pink"
                    >View Request</RouterLink
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      class="modal fade"
      id="staticBackdrop"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      aria-labelledby="staticBackdropLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="staticBackdropLabel">
              Request to
              {{
                influencers.find((inf) => inf.id === selectedInfluencerId)
                  ?.name
              }}:
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div
              v-for="campaign in userCampaigns"
              :key="campaign.id"
              class="form-check"
            >
              <input
                class="form-check-input"
                type="checkbox"
                :id="'campaign-' + campaign.id"
                :value="campaign.id"
                v-model="selectedCampaigns"
              />
              <label class="form-check-label" :for="'campaign-' + campaign.id">
                {{ campaign.name }}
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="button button-pink"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="button button-blue"
              @click="submitRequest()"
            >
              Submit Request
            </button>
          </div>
        </div>
      </div>
    </div>
    <SponsorFooter />
  </body>
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
.container {
  position: relative;
  z-index: 1;
}
</style>
