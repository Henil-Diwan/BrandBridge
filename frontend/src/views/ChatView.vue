<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import InfluencerHeader from "@/components/InfluencerHeader.vue";
import SponsorHeader from "@/components/SponsorHeader.vue";
import AdminHeader from "@/components/AdminHeader.vue";
import SponsorFooter from "@/components/SponsorFooter.vue";
import InfluencerFooter from "@/components/InfluencerFooter.vue";
import AdminFooter from "@/components/AdminFooter.vue";
let route = useRoute();
let router = useRouter();
let current_user = ref({
  user_id: 0,
  username: "",
  email: "",
  type: "",
});
let current_sponsor = ref({});
let current_influencer = ref({});
let messages = ref([]);
let person1 = ref("");
let person2 = ref("");
let id = ref(0);
let message = ref("");
onMounted(async () => {
  try {
    document.title = `BrandBridge | Chat`;
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
    if (current_user.value.type == "influencer") {
      current_influencer.value = response.data.current_influencer;
      id.value = current_influencer.value.id;
    } else if (current_user.value.type == "sponsor") {
      current_sponsor.value = response.data.current_sponsor;
      id.value = current_sponsor.value.id;
    }
    const response2 = await axios.get(
      `http://127.0.0.1:5001/chat/${route.params.chatter1}/${route.params.chatter2}`,
      {}
    );
    console.log(response2);
    messages.value = response2.data.messages;
    person1.value = response2.data.person1_name;
    person2.value = response2.data.person2_name;
    console.log(messages.value);
    if (
      route.params.chatter1 != current_user.value.user_id &&
      route.params.chatter2 != current_user.value.user_id
    ) {
      router.push("/");
    }
  } catch (err) {
    router.push("/login");
  }
});
const sendMessage = async () => {
  try {
    console.log(
      route.params.chatter1 == current_user.value.user_id
        ? route.params.chatter2
        : route.params.chatter1
    );
    const messageData = {
      sender_id: current_user.value.user_id,
      receiver_id:
        route.params.chatter1 == current_user.value.user_id
          ? route.params.chatter2
          : route.params.chatter1,
      message: message.value,
      sender_type: current_user.value.type,
      receiver_type: "",
    };
    const response_send = await axios.post(
      `http://127.0.0.1:5001/send_message`,
      messageData
    );
    toast("Message Sent!", {
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
  <div v-if="current_user.type == 'influencer'">
    <InfluencerHeader />
  </div>
  <div v-else-if="current_user.type == 'sponsor'">
    <SponsorHeader />
  </div>
  <div v-else>
    <AdminHeader />
  </div>
  <div class="wrapper my-5">
    <div class="container d-flex justify-content-center">
      <div class="row1">
        <div class="chat-container">
          <h3>Chat between {{ person1 }} and {{ person2 }}</h3>
          <input
            type="text"
            v-model="message"
            placeholder="Type your message..."
            rows="3"
            class="message-input mt-3"
          />
          <br />
          <button @click="sendMessage" class="button button-blue mb-3">
            Send
          </button>
          <div class="messages">
            <h4 v-if="messages.length == 0">No Current Chats</h4>
            <div
              v-else
              v-for="(msg, index) in messages"
              :key="msg.timestamp"
              class="message-box"
              :class="{
                'message-left': msg.sender_id !== current_user.user_id,
                'message-right': msg.sender_id === current_user.user_id,
              }"
            >
              <div class="ad_card">
                <div class="card-body">
                  <p class="card-text">{{ msg.sender_name }}</p>
                  <p class="card-text">{{ msg.message }}</p>
                  <p class="card-text">{{ msg.timestamp }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="current_user.type == 'influencer'">
    <InfluencerFooter />
  </div>
  <div v-else-if="current_user.type == 'sponsor'">
    <SponsorFooter />
  </div>
  <div v-else>
    <AdminFooter />
  </div>
</template>
<style scoped>
.back {
  text-align: center;
  font-size: small;
  margin-top: 25px;
}
h4 {
  font-size: large;
}
.ad_card {
  border: 2px solid #784ba887;
  border-radius: 10px;
  overflow: hidden;
  background: white;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 60%;
}
.row1 {
  border-radius: 10px;
  background: white;
  width: 900px;
  padding: 20px;
  box-shadow: 20px 20px 30px 1px rgba(0, 0, 0, 0.2);
}
.button {
  text-decoration: none;
  border-radius: 5px;
  color: white;
  transition: 0.4s;
  margin-top: 35px;
  padding: 7px;
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
  color: white;
}
.message-input {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 2px solid #784ba887;
  border-radius: 10px;
  color: #333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}
.messages {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.message-box {
  display: flex;
  justify-content: flex-start;
}
.message-left {
  justify-content: flex-start;
}
.message-right {
  justify-content: flex-end;
}
</style>
