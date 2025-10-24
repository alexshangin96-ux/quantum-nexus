<template>
  <div class="particle-background">
    <div 
      v-for="i in particleCount" 
      :key="i" 
      class="particle"
      :style="getParticleStyle(i)"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const particleCount = ref(50)
const particles = ref<Array<{
  x: number
  y: number
  vx: number
  vy: number
  size: number
  opacity: number
  color: string
}>>([])

const colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff88']

const getParticleStyle = (index: number) => {
  const particle = particles.value[index]
  if (!particle) return {}
  
  return {
    left: particle.x + 'px',
    top: particle.y + 'px',
    width: particle.size + 'px',
    height: particle.size + 'px',
    backgroundColor: particle.color,
    opacity: particle.opacity,
    animationDelay: (index * 0.1) + 's'
  }
}

const initParticles = () => {
  particles.value = []
  
  for (let i = 0; i < particleCount.value; i++) {
    particles.value.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      size: Math.random() * 3 + 1,
      opacity: Math.random() * 0.5 + 0.2,
      color: colors[Math.floor(Math.random() * colors.length)]
    })
  }
}

const animateParticles = () => {
  particles.value.forEach(particle => {
    particle.x += particle.vx
    particle.y += particle.vy
    
    // Wrap around screen
    if (particle.x < 0) particle.x = window.innerWidth
    if (particle.x > window.innerWidth) particle.x = 0
    if (particle.y < 0) particle.y = window.innerHeight
    if (particle.y > window.innerHeight) particle.y = 0
    
    // Fade in/out
    particle.opacity += (Math.random() - 0.5) * 0.02
    particle.opacity = Math.max(0.1, Math.min(0.7, particle.opacity))
  })
}

let animationId: number

onMounted(() => {
  initParticles()
  
  const animate = () => {
    animateParticles()
    animationId = requestAnimationFrame(animate)
  }
  
  animate()
  
  // Reinitialize on resize
  window.addEventListener('resize', initParticles)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  window.removeEventListener('resize', initParticles)
})
</script>

<style scoped>
.particle-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.particle {
  position: absolute;
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { 
    transform: translateY(0px) rotate(0deg); 
    opacity: 0.2; 
  }
  50% { 
    transform: translateY(-20px) rotate(180deg); 
    opacity: 0.8; 
  }
}
</style>