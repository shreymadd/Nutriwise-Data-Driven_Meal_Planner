<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-primary-50 to-green-100">
    <nav class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-primary-600">🥗 NutriWise</h1>
            <span class="ml-2 text-sm text-gray-500">Smart Meal Planner v2.0</span>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
              Home
            </router-link>
            <router-link to="/planner" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
              Meal Planner
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>

    <footer class="bg-white border-t mt-12">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <p class="text-center text-gray-500 text-sm">
          © 2024 NutriWise - Powered by Vue.js, Tailwind CSS & Supabase
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
