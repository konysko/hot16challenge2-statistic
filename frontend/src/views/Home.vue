<template>
  <div class="chart">
    <line-chart
      v-if="loaded"
      label="Całkowita zebrana kwota"
      :chart-data="dataValues"
      :chart-labels="dataLabels"
    ></line-chart>
  </div>
</template>

<script>
import moment from 'moment';

import LineChart from '@/components/LineChart.vue';

export default {
  name: 'Home',
  components: {
    LineChart
  },
  data() {
    return {
      dataValues: null,
      dataLabels: null,
      loaded: false
    };
  },
  mounted() {
    this.requestStatistic();
  },
  methods: {
    async requestStatistic() {
      const response = await fetch('./statistic.json', {
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json'
        }
      });
      const statistic = await response.json();

      console.log(statistic);

      this.dataValues = statistic.map((timeSlot) => timeSlot.total_sum_amount);
      this.dataLabels = statistic.map((timeSlot) => moment(timeSlot.date).format('DD-MM-YYYY'));

      this.loaded = true;
    }
  }
};
</script>

<style scoped>
.chart {
  height: 80%;
}
</style>
