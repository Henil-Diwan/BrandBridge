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
let campaigns = ref([]);
onMounted(async () => {
  try {
    document.title = `BrandBridge | Saved`;
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
    const response2 = await axios.get("http://127.0.0.1:5001/saved_campaigns", {
      params: { influencer_id: current_influencer.value.id },
    });
    console.log(response2);
    campaigns.value = response2.data.campaigns;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
const submitRequest = async (campaign_id) => {
  const requestdata = {
    campaign_id: campaign_id,
    influencer_id: current_influencer.value.id,
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
    influencer_id: current_influencer.value.id,
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
    influencer_id: current_influencer.value.id,
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
    <div class="container">
      <div class="my-5 text-white">
        <h3>Saved Campaigns</h3>
      </div>
    </div>
    <div v-if="campaigns.length == 0" class="my-5 text-center text-white">
      <h5>No Saved Campaigns</h5>
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
                    class="link-dark"
                    :to="`/show_campaign/${campaign.id}`"
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
                  From: {{ campaign.start_date }} <br />
                  To: {{ campaign.end_date }}
                </li>
                <li class="list-group-item">
                  <i class="bi bi-eye-fill"></i> {{ campaign.views }}
                </li>
              </ul>
              <div class="card-body text-center">
                <RouterLink
                  :to="`/show_campaign/${campaign.id}`"
                  class="button button-blue"
                  >View Request</RouterLink
                >
                <button
                  type="button"
                  class="button button-pink"
                  @click="submitRequest(campaign.id)"
                >
                  Request
                </button>
                <button
                  v-if="campaign.saved"
                  type="button"
                  class="button button-blue"
                  @click="unsaveCampaign(campaign.id)"
                >
                  Unsave
                </button>
                <button
                  v-else
                  type="button"
                  class="button button-blue"
                  @click="saveCampaign(campaign.id)"
                >
                  Save
                </button>
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
