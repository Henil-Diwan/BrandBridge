<template>
  <div class="d-none d-md-inline blue-circle"></div>
  <div class="d-none d-md-inline blue-circle-2"></div>
  <div class="d-none d-md-inline purple-circle-2"></div>
  <div class="d-none d-md-inline purple-circle"></div>
  <div class="d-none d-md-inline pink-circle"></div>
  <nav class="navbar navbar-expand-lg d-flex flex-column navbar-dark">
    <div class="container-fluid">
      <img
              :src="`http://127.0.0.1:5001/uploads/Logo.png`"
              alt="Profile Picture"
              class="navbar-brand"
              width="150"
            />
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mx-auto mb-2 mb-lg-0">
          <li class="nav-item nav-item-pink">
            <RouterLink class="nav-link active" aria-current="page" to="/"
              >Home</RouterLink
            >
          </li>
          <li class="nav-item mx-3 nav-item-blue">
            <RouterLink class="nav-link" to="/influencer_profile"
              >Profile</RouterLink
            >
          </li>
          <li class="nav-item mx-3 nav-item-purple">
            <RouterLink class="nav-link" to="/influencer_stats"
              >Stats</RouterLink
            >
          </li>
          <li class="nav-item mx-3 nav-item-blue">
            <RouterLink class="nav-link" to="/all_campaigns"
              >All Campaigns</RouterLink
            >
          </li>
          <li class="nav-item mx-3 nav-item-pink">
            <RouterLink class="nav-link" to="/saved_campaigns"
              >Saved Campaigns</RouterLink
            >
          </li>
          <li class="nav-item mx-3 nav-item-purple">
            <RouterLink class="nav-link" to="/search">Search</RouterLink>
          </li>
          <li class="nav-item mx-3 nav-item-pink">
            <RouterLink class="nav-link" to="/logout">Log Out</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar a {
  font-weight: 500;
  color: white;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 1rem;
  background-size: 250%;
  border-radius: 10%;
  transition: all 0.4s;
  height: 50px;
  display: flex;
  align-items: center;
}
.nav-item:hover {
  background-position: 100%;
}

.nav-item-purple {
  background-image: linear-gradient(
    120deg,
    transparent 0%,
    transparent 50%,
    #784ba8 50%
  );
}
.nav-item-blue {
  background-image: linear-gradient(
    120deg,
    transparent 0%,
    transparent 50%,
    #5c9df1 50%
  );
}

.nav-item-pink {
  background-image: linear-gradient(
    120deg,
    transparent 0%,
    transparent 50%,
    #fa709a 50%
  );
}
.bg {
  padding: 15px;
  background-image: linear-gradient(
    45deg,
    #fa709a 0%,
    #fa709a 20%,
    #5c9df1 20%,
    #5c9df1 40%,
    #784ba8 40%,
    #784ba8 60%,
    #fa709a 60%,
    #fa709a 80%,
    #5c9df1 80%,
    #5c9df1 100%
  );
  border-radius: 5%;
}

.link {
  color: white;
  text-decoration: none;
  transition: 0.5s;
}
.link-dark {
  color: #40414a;
  text-decoration: none;
  transition: 0.5s;
}
.link,
.link-dark:hover {
  text-decoration: underline;
}
.link-blue:hover {
  color: #5c9df1;
}
.link-purple:hover {
  color: #784ba8;
}
.link-pink:hover {
  color: #fa709a;
}
</style>
