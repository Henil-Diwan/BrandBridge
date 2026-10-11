<template>
  <div class="container">
    <footer class="py-3 my-4 text-white">
      <ul class="nav justify-content-center pb-3 mb-3">
        <li class="nav-item">
          <RouterLink to="/" class="px-2 link link-blue">Home</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/sponsor_profile" class="px-2 link link-pink"
            >Profile</RouterLink
          >
        </li>
        <li class="nav-item">
          <RouterLink to="/sponsor_stats" class="px-2 link link-purple"
            >Stats</RouterLink
          >
        </li>
        <li class="nav-item">
          <RouterLink to="/my_campaigns" class="px-2 link link-blue"
            >My Campaigns</RouterLink
          >
        </li>
        <li class="nav-item">
          <RouterLink to="/create" class="px-2 link link-pink"
            >Create</RouterLink
          >
        </li>
        <li class="nav-item">
          <RouterLink to="/search" class="px-2 link link-purple"
            >Search</RouterLink
          >
        </li>
        <li class="nav-item">
          <RouterLink to="/logout" class="px-2 link link-blue"
            >Logout</RouterLink
          >
        </li>
      </ul>
      <p class="text-center">&copy; 2022 Company, Inc</p>
    </footer>
  </div>
</template>

<style scoped>
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
