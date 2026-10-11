<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import AdminHeader from "@/components/AdminHeader.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import AdminFooter from "@/components/AdminFooter.vue";
let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});
let campaigns = ref([]);
let influencers = ref([]);
let sponsors = ref([]);
const categories = [
  "All Categories",
  "Any",
  "Health & Wellness",
  "Travel & Food",
  "Finance & Business",
  "Technology",
  "Entertainment",
  "Gaming",
  "Education",
  "Lifestyle",
  "Other",
];
const searchQuery = ref("");
const selectedCategory = ref("All Categories");
onMounted(async () => {
  try {
    document.title = `BrandBridge | Admin`;
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
    const response2 = await axios.get("http://127.0.0.1:5001/admin_flagged", {
      params: {},
    });
    console.log(response2);
    campaigns.value = response2.data.campaigns;
    influencers.value = response2.data.influencers;
    sponsors.value = response2.data.sponsors;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});
const filteredCampaigns = computed(() => {
  return campaigns.value.filter((campaign) => {
    const searchMatch = campaign.name
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase());
    const categoryMatch =
      selectedCategory.value === "All Categories" ||
      campaign.category === selectedCategory.value;
    return searchMatch && categoryMatch;
  });
});
const filteredInfluencers = computed(() => {
  return influencers.value.filter((influencer) => {
    const searchMatch = influencer.name
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase());
    const categoryMatch =
      selectedCategory.value === "All Categories" ||
      influencer.category === selectedCategory.value;
    return searchMatch && categoryMatch;
  });
});
const filteredSponsors = computed(() => {
  return sponsors.value.filter((sponsor) => {
    const searchMatch = sponsor.name
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase());
    const categoryMatch =
      selectedCategory.value === "All Categories" ||
      sponsor.industry === selectedCategory.value;
    return searchMatch && categoryMatch;
  });
});
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
const unflagInfluencer = async (influencerId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/unflag_influencer/${influencerId}`
    );
    toast("Influencer Unflagged!", {
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
const unflagSponsor = async (sponsorId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/unflag_sponsor/${sponsorId}`
    );
    toast("Sponsor Unflagged!", {
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
  <AdminHeader />
  <div class="container mt-4">
    <h1 class="text-white">Flagged</h1>
    <div class="mb-4">
      <input
        type="text"
        class="form-control mb-2"
        placeholder="Search campaigns..."
        v-model="searchQuery"
      />
      <select class="form-select" v-model="selectedCategory">
        <option
          v-for="category in categories"
          :key="category"
          :value="category"
        >
          {{ category }}
        </option>
      </select>
    </div>
    <div id="sponsorGrid" class="row g-3">
      <h3 class="my-3 text-white">Sponsors</h3>
      <div
        class="col-md-4 sponsor-card"
        v-for="sponsor in filteredSponsors"
        :key="sponsor.id"
      >
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ sponsor.name }}</h5>
            <p class="card-text">Budget: ${{ sponsor.budget }}</p>
            <p class="card-text">Industry: {{ sponsor.industry }}</p>
            <button
              class="button button-blue"
              @click="unflagSponsor(sponsor.id)"
            >
              Unflag
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="campaignGrid" class="row g-5 mt-3">
      <h3 class="my-3 text-white">Campaigns</h3>
      <div
        class="col-md-4 campaign-card"
        v-for="campaign in filteredCampaigns"
        :key="campaign.id"
      >
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">
              <router-link
                :to="`/show_campaign/${campaign.id}`"
                class="link-dark"
              >
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
            <p class="card-text">By: {{ campaign.by }}</p>
            <p class="card-text">Visibility: {{ campaign.visibility }}</p>
            <button
              class="button button-pink"
              @click="unflagCampaign(campaign.id)"
            >
              Unflag
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="influencerGrid" class="row g-5 mt-3">
      <h3 class="my-3 text-white">Influencers</h3>
      <div
        class="col-md-4 influencer-card"
        v-for="influencer in filteredInfluencers"
        :key="influencer.id"
      >
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">
              <RouterLink
                :to="`/view_influencer/${influencer.id}`"
                class="link-dark"
                >{{ influencer.name }}</RouterLink
              >
            </h5>
            <p class="card-text">{{ influencer.about }}</p>
            <p class="card-text">Category: {{ influencer.category }}</p>
            <p class="card-text">Niche: {{ influencer.niche }}</p>
            <p class="card-text">Reach: {{ influencer.reach }}</p>
            <p class="card-text">Average Rating: {{ influencer.rating }}</p>
            <button
              class="button button-blue"
              @click="unflagInfluencer(influencer.id)"
            >
              Unflag
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <AdminFooter />
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
</style>
