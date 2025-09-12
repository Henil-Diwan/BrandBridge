<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import AdminHeader from "@/components/AdminHeader.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});

let campaigns = ref([])
const categories = [
  'All Categories',
  'Any',
  'Health & Wellness',
  'Travel & Food',
  'Finance & Business',
  'Technology',
  'Entertainment',
  'Gaming',
  'Education',
  'Lifestyle',
  'Other'
];

const searchQuery = ref('');
const selectedCategory = ref('All Categories');


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

    const response2 = await axios.get("http://127.0.0.1:5001/admin_campaigns", {
      params: {}, // Pass user_id as a query parameter
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    campaigns.value = response2.data.campaigns;
    console.log(campaigns.value);
    
  } catch (err) {
    console.log(err);

    router.push("/login");
  }
});

const filteredCampaigns = computed(() => {
  return campaigns.value.filter((campaign) => {
    const searchMatch = campaign.name.toLowerCase().includes(searchQuery.value.toLowerCase());
    const categoryMatch = selectedCategory.value === 'All Categories' || campaign.category === selectedCategory.value;
    return searchMatch && categoryMatch;
  });
});

const flagCampaign = async (campaignId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/flag_campaign/${campaignId}`
    );
    toast("Campaign Flagged!", {
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

const unflagCampaign = async (campaignId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/unflag_campaign/${campaignId}`
    );
    toast("Campaign Unflagged!", {
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
    <AdminHeader />

    <h2>All Campaigns</h2>

    <div class="mb-4">
        <input
          type="text"
          class="form-control mb-2"
          placeholder="Search campaigns..."
          v-model="searchQuery"
        />
        <select
          class="form-select"
          v-model="selectedCategory"
        >
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>

      <div id="campaignGrid" class="row g-5">
        <div
          v-for="campaign in filteredCampaigns"
          :key="campaign.id"
          class="col-md-4 campaign-card"
        >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">
                <router-link :to="`/campaign/${campaign.id}`" class="link-dark">
                  {{ campaign.name }}
                </router-link>
              </h5>
              <p class="card-text">{{ campaign.desc }}</p>
              <p class="card-text">Budget: {{ campaign.budget }}</p>
              <p class="card-text">Preferred Category: {{ campaign.category }}</p>
              <p class="card-text">Goals: {{ campaign.goals }}</p>
              <p class="card-text">Start Date: {{ campaign.start_date }}</p>
              <p class="card-text">End Date: {{ campaign.end_date }}</p>
              <p class="card-text">Status: {{ campaign.status }}</p>
              <p class="card-text">Visibility: {{ campaign.visibility }}</p>
              <button v-if="campaign.flag === 'No'" class="btn btn-danger" @click="flagCampaign(campaign.id)" >
                Flag
              </button>
              <button v-else class="btn btn-primary" @click="unflagCampaign(campaign.id)">
                Unflag
              </button>
            </div>
          </div>
        </div>
      </div>

      

    
  </main>
</template>
