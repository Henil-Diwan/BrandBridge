<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import SponsorHeader from "@/components/SponsorHeader.vue";
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
let campaigns = ref([]);

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

    const response2 = await axios.get(
      "http://127.0.0.1:5001/all_campaigns",
      {
        params: { influencer_id: current_influencer.value.id }, // Pass user_id as a query parameter
      }
    );

    console.log(response2);

    // Extract data from the response and assign it to the respective variables
    campaigns.value = response2.data.campaigns;

  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});

const submitRequest = async (campaign_id) => {
  const requestdata = {
    campaign_id: campaign_id,
    influencer_id: current_influencer.value.id
    };

    try {
    const response_request = await axios.post(
      "http://127.0.0.1:5001/request_by_influencer",
      requestdata,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );

    toast("Request Sent Successfully", {
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


const saveCampaign = async (campaign_id) => {
  const requestdata = {
    campaign_id: campaign_id,
    influencer_id: current_influencer.value.id
    };

    try {
    const save_response = await axios.post(
      "http://127.0.0.1:5001/save_campaign",
      requestdata,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );

    toast("Campaign Saved Successfully", {
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

const unsaveCampaign = async (campaign_id) => {
  const requestdata = {
    campaign_id: campaign_id,
    influencer_id: current_influencer.value.id
    };

    try {
    const unsave_response = await axios.post(
      "http://127.0.0.1:5001/unsave_campaign",
      requestdata,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("user")?.access_token}`,
        },
      }
    );

    toast("Campaign Unsaved Successfully", {
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

    <h3 class="mt-5">All Campaigns</h3>
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
              <RouterLink to="/" class="btn btn-primary"
                >View Request</RouterLink
              >
              <button
                    type="button"
                    class="btn btn-warning mx-2"
                    @click="submitRequest(campaign.id)"
                  >
                    Request
                  </button>
                  <button
                    v-if="campaign.saved"
                    type="button"
                    class="btn btn-danger my-2"
                    @click="unsaveCampaign(campaign.id)"
                  >
                    Unsave
                  </button>
                  <button
                    v-else
                    type="button"
                    class="btn btn-danger my-2"
                    @click="saveCampaign(campaign.id)"
                  >
                    Save
                  </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No Campaigns found.</p>
    </div>
  </main>
</template>
