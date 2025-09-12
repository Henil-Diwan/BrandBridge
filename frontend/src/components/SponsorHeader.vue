<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
<div class="container-fluid">
  <RouterLink class="navbar-brand" to="/">Sponsor</RouterLink>
  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
      <li class="nav-item">
          <RouterLink class="nav-link active" to="/">Home</RouterLink>
      </li>
      <li class="nav-item">
          <RouterLink class="nav-link active" to="/sponsor_profile">Profile</RouterLink>
      </li>
      <li class="nav-item">
          <RouterLink class="nav-link active" to="/sponsor_stats">Stats</RouterLink>
      </li>
      <li class="nav-item">
          <RouterLink class="nav-link active" to="/my_campaigns">My Campaigns</RouterLink>
      </li>
      <li class="nav-item">
          <RouterLink class="nav-link active" to="/create">Create</RouterLink>
      </li>
      <li class="nav-item">
          <RouterLink class="nav-link active" to="/logout">Logout</RouterLink>
      </li>
      
      <li class="nav-item">
          <RouterLink class="nav-link active" to="/search">Search</RouterLink>
      </li>
  </ul>
  </div>
</div>
</nav>

</template>