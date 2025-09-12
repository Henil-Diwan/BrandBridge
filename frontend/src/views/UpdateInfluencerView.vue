<script setup>
import { ref,onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

let route = useRoute();

let id = ref(-1);
let name = ref("");
let about = ref("");
let category = ref("");
let niche = ref("");
let reach = ref(0);
let fileInput = ref(null);
let files = ref();
const router = useRouter();
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

function handleFileChange() {
    files.value = fileInput.value?.files
}

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

    const response2 = await axios.get("http://127.0.0.1:5001/update_influencer", {
      params: { influencer_id: current_influencer.value.id }, // Pass user_id as a query parameter
    });

    console.log(response2);

    // Extract data from the response and assign it to the respective variables
    id.value = response2.data.current_influencer.id;
    name.value = response2.data.current_influencer.name;
    about.value = response2.data.current_influencer.about;
    category.value = response2.data.current_influencer.category;
    niche.value = response2.data.current_influencer.niche;
    reach.value = response2.data.current_influencer.reach;
    
  } catch (err) {
    console.log(err);
    router.push("/login");
  }
});

let updateInfluencer = async () => {
  try {
    const formData = new FormData();
    formData.append("influencer_id", id.value);
    formData.append("name", name.value);
    formData.append("about", about.value);
    formData.append("category", category.value);
    formData.append("niche", niche.value);
    formData.append("reach", reach.value);
    formData.append("creator", route.params.creator);

    const file = files.value ? files.value[0] : null;
    console.log(file);

    if (file) {
      formData.append("ProfilePic", file); // Append the file
    }
    
    console.log("selected file",file)

    const response = await axios.post(
      "http://127.0.0.1:5001/update_influencer",
      formData
    );

    console.log(response);

    toast("Influencer Updated Successfully", {
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
      onClose: () => {
        router.push("/influencerhome");
      },
      autoClose: 1000,
    });
  } catch (error) {
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

  <div class="register">
    <h1>Update Details of {{ current_influencer.name }}</h1>
  </div>

  <form @submit.prevent="updateInfluencer">
    <div class="mb-3">
      <label for="exampleInputUsername1" class="form-label">Name</label>
      <input
        v-model="name"
        type="text"
        class="form-control"
        id="exampleInputUsername1"
        aria-describedby="usernamelHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">About</label>
      <input
        v-model="about"
        type="text"
        class="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputType1" class="form-label">Category</label>
      <select
        v-model="category"
        class="form-select"
        aria-label="exampleInputType1"
      >
        <option value="" disabled selected>Default</option>
        <option value="Health & Wellness">Health & Wellness</option>
        <option value="Travel & Food">Travel & Food</option>
        <option value="Finance & Business">Finance & Business</option>
        <option value="Technology">Technology</option>
        <option value="Entertainment">Entertainment</option>
        <option value="Gaming">Gaming</option>
        <option value="Education">Education</option>
        <option value="Lifestyle">Lifestyle</option>
        <option value="Other">Other</option>
      </select>
    </div>
    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">Niche</label>
      <input
        v-model="niche"
        type="text"
        class="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
      />
    </div>
    <div class="mb-3">
      <label for="exampleInputEmail1" class="form-label">Reach</label>
      <input
        v-model="reach"
        type="number"
        class="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
      />
    </div>

    <div class="mb-3">
      <label for="profilePic" class="form-label">Profile Picture</label>
      <input ref="fileInput" type="file" @change="handleFileChange" />
    </div>

    <button type="submit" class="btn btn-primary">Update</button>
  </form>
</template>
