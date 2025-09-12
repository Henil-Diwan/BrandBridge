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
let influencers = ref([]);
let campaigns = ref([]);
let selectedCampaigns = ref([]);
let userCampaigns = ref([]);

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
      "http://127.0.0.1:5001/sponsor_dashboard",
      {
        params: { user_id: current_user.value.user_id }, // Pass user_id as a query parameter
      }
    );

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

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
    influencer_id: infid,
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
</script>

<template>
  <main>
    <SponsorHeader />
    <h2>Hello {{ current_sponsor.name }}</h2>

    <!-- Influencers Section -->
    <h3>Top Voices in Your Industry</h3>
    <div v-if="influencers.length > 0">
      <div class="row">
        <div
          class="col-lg-3"
          v-for="influencer in influencers"
          :key="influencer.id"
        >
          <div class="card" style="width: 18rem">
            <div class="card-body">
              <h5 class="card-title">
                <RouterLink :to="`/view_influencer/${influencer}`">{{ influencer.name }}</RouterLink>
              </h5>
              <p class="card-text">
                {{ influencer.about }}
              </p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                Category: {{ influencer.category }}
              </li>
              <li class="list-group-item">Niche: {{ influencer.niche }}</li>
              <li class="list-group-item">Reach: {{ influencer.reach }}</li>
              <li class="list-group-item">Rating: {{ influencer.rating }}</li>
              <li class="list-group-item">Views: {{ influencer.views }}</li>
            </ul>
            <div class="card-body text-center">
              <RouterLink to="/" class="btn btn-primary mx-2"
                >View Profile</RouterLink
              >
              <button
                type="button"
                class="btn btn-warning mx-2"
                :data-bs-target="'#requestModal-' + influencer.id"
                data-bs-toggle="modal"
              >
                Request
              </button>

              <RouterLink
                :to="`/rate/${influencer.id}`"
                class="btn btn-danger mx-2"
                >Rate</RouterLink
              >
            </div>
          </div>

          <div
  class="modal fade"
  :id="'requestModal-' + influencer.id"
  tabindex="-1"
  aria-labelledby="'requestModalLabel-' + influencer.id"
  aria-hidden="true"
>
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" :id="'requestModalLabel-' + influencer.id">
          Request to {{ influencer.name }}:
        </h5>
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
          <label
            class="form-check-label"
            :for="'campaign-' + campaign.id"
          >
            {{ campaign.name }}
          </label>
        </div>
      </div>
      <div class="modal-footer">
        <button
          type="button"
          class="btn btn-secondary"
          data-bs-dismiss="modal"
        >
          Close
        </button>
        <button
          type="button"
          class="btn btn-primary"
          @click="submitRequest(influencer.id)"
        >
          Submit Request
        </button>
      </div>
    </div>
  </div>
</div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No Influencers found in your industry.</p>
    </div>

    <h3 class="mt-5">Current Campaigns in Your Industry</h3>
    <div v-if="campaigns.length > 0">
      <div class="row">
        <div class="col-lg-3" v-for="campaign in campaigns" :key="campaign.id">
          <div class="card" style="width: 18rem">
            <div class="card-body">
              <h5 class="card-title">
                <RouterLink to="/">{{ campaign.name }}</RouterLink>
              </h5>
              <p class="card-text">
                {{ campaign.desc }}
              </p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                Preferred Category: {{ campaign.category }}
              </li>
              <li class="list-group-item">Goals: {{ campaign.goals }}</li>
              <li class="list-group-item">Budget: {{ campaign.budget }}</li>
              <li class="list-group-item">Start: {{ campaign.start_date }}</li>
              <li class="list-group-item">End: {{ campaign.end_date }}</li>
              <li class="list-group-item">Views: {{ campaign.views }}</li>
            </ul>
            <div class="card-body text-center">
              <RouterLink to="/" class="btn btn-primary mx-2"
                >View Request</RouterLink
              >
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No Campaigns found in your industry.</p>
    </div>
  </main>
</template>
