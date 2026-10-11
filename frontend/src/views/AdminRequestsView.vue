<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import AdminHeader from "@/components/AdminHeader.vue";
import AdminFooter from "@/components/AdminFooter.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});
let sponsors = ref([]);
const categories = [
  "All Categories",
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
    const response2 = await axios.get(
      "http://127.0.0.1:5001/pending_sponsors",
      {
        params: {},
      }
    );
    console.log(response2);
    sponsors.value = response2.data.sponsors;
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
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
  <AdminHeader />
  <div class="container mt-4">
    <h1 class="text-white">Pending Registration Requests:</h1>
    <div class="mb-4">
      <input
        type="text"
        id="searchInput"
        class="form-control mb-2"
        placeholder="Search sponsors..."
        v-model="searchQuery"
      />
      <select
        id="categoryFilter"
        class="form-select"
        v-model="selectedCategory"
      >
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
              @click="approveSponsor(sponsor.id)"
            >
              Approve
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
