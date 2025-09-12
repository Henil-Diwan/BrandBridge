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

let sponsors = ref([])
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

    const response2 = await axios.get("http://127.0.0.1:5001/pending_sponsors", {
      params: {}, // Pass user_id as a query parameter
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables

    sponsors.value = response2.data.sponsors;
    
  } catch (err) {
    console.log(err);

    router.push("/login");
  }
});

const filteredSponsors = computed(() => {
  return sponsors.value.filter((sponsor) => {
    const searchMatch = sponsor.name.toLowerCase().includes(searchQuery.value.toLowerCase());
    const categoryMatch = selectedCategory.value === 'All Categories' || sponsor.industry === selectedCategory.value;
    return searchMatch && categoryMatch;
  });
});

const approveSponsor = async (sponsorId) => {
  try {
    console.log(sponsorId);
    
    const response_flag = await axios.post(
      `http://127.0.0.1:5001/approve_sponsor/${sponsorId}`
    );
    toast("Sponsor Approved!", {
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

    <h2>Pending Sponsors Register Requests</h2>

    <div class="mb-4">
        <input
          type="text"
          class="form-control mb-2"
          placeholder="Search sponsors..."
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

      <div id="sponsorGrid" class="row g-5">
        <div
          v-for="sponsor in filteredSponsors"
          :key="sponsor.id"
          class="col-md-4 sponsor-card"
        >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">
                  {{ sponsor.name }}

              </h5>
              <p class="card-text">Budget: {{ sponsor.budget }}</p>
              <p class="card-text">Industry: {{ sponsor.industry }}</p>
              <button class="btn btn-primary" @click="approveSponsor(sponsor.id)" >
                Approve
              </button>
            </div>
          </div>
        </div>
      </div>

      

    
  </main>
</template>
