<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <RouterLink class="navbar-brand" to="/">Admin</RouterLink>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
            <RouterLink class="nav-link active" to="/">Home</RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink class="nav-link active" to="/admin_sponsors">Sponsors</RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink class="nav-link active" to="/admin_campaigns">Campaigns</RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink class="nav-link active" to="/admin_influencers">Influencers</RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink class="nav-link active" to="/admin_flagged">Flagged</RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink class="nav-link active" to="/admin_requests">Requests</RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink class="nav-link active" to="/logout">Logout</RouterLink>
        </li>
    </ul>
    </div>
  </div>
</nav>
</template>