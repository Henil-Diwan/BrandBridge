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

let influencers = ref([])
const categories = [
  'All Categories',
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

    const response2 = await axios.get("http://127.0.0.1:5001/admin_influencers", {
      params: {}, // Pass user_id as a query parameter
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    influencers.value = response2.data.influencers;
    
  } catch (err) {
    console.log(err);

    router.push("/login");
  }
});

const filteredInfluencers = computed(() => {
  return influencers.value.filter((influencer) => {
    const searchMatch = influencer.name.toLowerCase().includes(searchQuery.value.toLowerCase());
    const categoryMatch = selectedCategory.value === 'All Categories' || influencer.category === selectedCategory.value;
    return searchMatch && categoryMatch;
  });
});

const flagInfluencer = async (influencerId) => {
  try {
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/flag_influencer/${influencerId}`
    );
    toast("Influencer Flagged!", {
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
</script>

<template>
  <main>
    <AdminHeader />

    <h2>All Influencers</h2>

    <div class="mb-4">
        <input
          type="text"
          class="form-control mb-2"
          placeholder="Search influencers..."
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

      <div id="influencerGrid" class="row g-5">
        <div
          v-for="influencer in filteredInfluencers"
          :key="influencer.id"
          class="col-md-4 influencer-card"
        >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">
                  {{ influencer.name }}

              </h5>
              <p class="card-text">{{ influencer.about }}</p>
              <p class="card-text">Category: {{ influencer.category }}</p>
              <p class="card-text">Niche: {{ influencer.niche }}</p>
              <p class="card-text">Reach: {{ influencer.reach }}</p>
              <p class="card-text">Rating: {{ influencer.rating }}</p>
              <button v-if="influencer.flag === 'No'" class="btn btn-danger" @click="flagInfluencer(influencer.id)" >
                Flag
              </button>
              <button v-else class="btn btn-primary" @click="unflagInfluencer(influencer.id)">
                Unflag
              </button>
            </div>
          </div>
        </div>
      </div>

      

    
  </main>
</template>
