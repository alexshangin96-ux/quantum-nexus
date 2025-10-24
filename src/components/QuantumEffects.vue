<template>
  <div class="quantum-effects">
    <!-- Quantum field lines -->
    <div class="field-lines">
      <div 
        v-for="i in 5" 
        :key="i" 
        class="field-line"
        :style="{ '--delay': i * 0.5 + 's' }"
      ></div>
    </div>
    
    <!-- Energy waves -->
    <div class="energy-waves">
      <div 
        v-for="i in 3" 
        :key="i" 
        class="energy-wave"
        :style="{ '--delay': i * 1 + 's' }"
      ></div>
    </div>
    
    <!-- Quantum sparks -->
    <div class="quantum-sparks">
      <div 
        v-for="i in 20" 
        :key="i" 
        class="spark"
        :style="getSparkStyle(i)"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const sparks = ref<Array<{
  x: number
  y: number
  vx: number
  vy: number
  life: number
  maxLife: number
}>>([])

const getSparkStyle = (index: number) => {
  const spark = sparks.value[index]
  if (!spark) return {}
  
  const opacity = spark.life / spark.maxLife
  
  return {
    left: spark.x + 'px',
    top: spark.y + 'px',
    opacity: opacity,
    animationDelay: (index * 0.1) + 's'
  }
}

const initSparks = () => {
  sparks.value = []
  
  for (let i = 0; i < 20; i++) {
    sparks.value.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2,
      life: Math.random() * 100,
      maxLife: 100
    })
  }
}

const animateSparks = () => {
  sparks.value.forEach(spark => {
    spark.x += spark.vx
    spark.y += spark.vy
    spark.life -= 0.5
    
    if (spark.life <= 0) {
      spark.x = Math.random() * window.innerWidth
      spark.y = Math.random() * window.innerHeight
      spark.life = spark.maxLife
      spark.vx = (Math.random() - 0.5) * 2
      spark.vy = (Math.random() - 0.5) * 2
    }
    
    // Wrap around screen
    if (spark.x < 0) spark.x = window.innerWidth
    if (spark.x > window.innerWidth) spark.x = 0
    if (spark.y < 0) spark.y = window.innerHeight
    if (spark.y > window.innerHeight) spark.y = 0
  })
}

let animationId: number

onMounted(() => {
  initSparks()
  
  const animate = () => {
    animateSparks()
    animationId = requestAnimationFrame(animate)
  }
  
  animate()
  
  window.addEventListener('resize', initSparks)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  window.removeEventListener('resize', initSparks)
})
</script>

<style scoped>
.quantum-effects {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2;
  overflow: hidden;
}

.field-lines {
  position: absolute;
  width: 100%;
  height: 100%;
}

.field-line {
  position: absolute;
  width: 2px;
  height: 100px;
  background: linear-gradient(to bottom, transparent, var(--quantum-primary), transparent);
  animation: field-flow 4s ease-in-out infinite;
  animation-delay: var(--delay);
}

.field-line:nth-child(1) { left: 10%; top: 20%; transform: rotate(15deg); }
.field-line:nth-child(2) { left: 30%; top: 60%; transform: rotate(-20deg); }
.field-line:nth-child(3) { left: 60%; top: 30%; transform: rotate(45deg); }
.field-line:nth-child(4) { left: 80%; top: 70%; transform: rotate(-30deg); }
.field-line:nth-child(5) { left: 50%; top: 10%; transform: rotate(60deg); }

@keyframes field-flow {
  0%, 100% { 
    opacity: 0.3; 
    transform: scaleY(0.5) rotate(var(--rotation, 0deg)); 
  }
  50% { 
    opacity: 1; 
    transform: scaleY(1.5) rotate(var(--rotation, 0deg)); 
  }
}

.energy-waves {
  position: absolute;
  width: 100%;
  height: 100%;
}

.energy-wave {
  position: absolute;
  width: 200px;
  height: 200px;
  border: 2px solid var(--quantum-primary);
  border-radius: 50%;
  animation: energy-pulse 3s ease-in-out infinite;
  animation-delay: var(--delay);
}

.energy-wave:nth-child(1) { 
  top: 20%; 
  left: 20%; 
  animation-duration: 3s; 
}
.energy-wave:nth-child(2) { 
  top: 50%; 
  right: 20%; 
  animation-duration: 4s; 
}
.energy-wave:nth-child(3) { 
  bottom: 20%; 
  left: 50%; 
  animation-duration: 5s; 
}

@keyframes energy-pulse {
  0% { 
    transform: scale(0.5); 
    opacity: 0.8; 
  }
  50% { 
    transform: scale(1.2); 
    opacity: 0.3; 
  }
  100% { 
    transform: scale(2); 
    opacity: 0; 
  }
}

.quantum-sparks {
  position: absolute;
  width: 100%;
  height: 100%;
}

.spark {
  position: absolute;
  width: 3px;
  height: 3px;
  background: var(--quantum-accent);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--quantum-accent);
  animation: spark-flicker 2s ease-in-out infinite;
}

@keyframes spark-flicker {
  0%, 100% { 
    opacity: 0.2; 
    transform: scale(0.5); 
  }
  50% { 
    opacity: 1; 
    transform: scale(1.5); 
  }
}

@media (max-width: 768px) {
  .field-line {
    height: 60px;
  }
  
  .energy-wave {
    width: 120px;
    height: 120px;
  }
  
  .spark {
    width: 2px;
    height: 2px;
  }
}
</style>