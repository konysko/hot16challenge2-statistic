<template>
  <div class="chart">
    <v-select
      color="#272727"
      item-color="#272727"
      :items="ranges"
      v-model="range"
      @change="onChangeRange"
      label="Range"
      outlined
    ></v-select>
    <line-chart
      v-if="loaded"
      :chart-total-amount-values="chartTotalAmountValues"
      :chart-video-count-values="chartVideoCountValues"
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
      chartTotalAmountValues: null,
      chartVideoCountValues: null,
      dataLabels: null,
      loaded: false,
      ranges: ['Hour', 'Day'],
      range: 'Day',
      statistic: null
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
      this.statistic = await response.json();

      this.setStatisticChartData(this.statistic, this.range);

      this.loaded = true;
    },
    setStatisticChartData(statistic, range) {
      const rangedStatistic = this.getRangesStatistic(statistic, range);

      this.chartTotalAmountValues = rangedStatistic.map((timeSlot) => timeSlot.total_sum_amount);
      this.chartVideoCountValues = rangedStatistic.map((timeSlot) => {
        const videoTitles = timeSlot.video_titles;
        return videoTitles ? videoTitles.length : 0;
      });
      this.dataLabels = rangedStatistic.map((timeSlot) => moment(timeSlot.date).format('DD-MM-YYYY'));
    },
    onChangeRange(range) {
      this.setStatisticChartData(this.statistic, range);
    },
    getRangesStatistic(statistic, range) {
      if (range === 'Hour') {
        return statistic;
      } else {
        return statistic.reduce((prev, curr) => {
          const length = prev.length;
          const prevItem = length && prev[length - 1];
          if (prevItem && moment(prevItem.date).format('DD-MM-YYYY') === moment(curr.date).format('DD-MM-YYYY')) {
            prevItem.total_sum_amount = curr.total_sum_amount;
            prevItem.video_thumbnails = this.concatVideoArrays(prevItem.video_thumbnails, curr.video_thumbnails);
            prevItem.video_titles = this.concatVideoArrays(prevItem.video_titles, curr.video_titles);
            prevItem.video_urls = this.concatVideoArrays(prevItem.video_urls, curr.video_urls);
          } else {
            prev.push({ ...curr });
          }
          return prev;
        }, []);
      }
    },
    concatVideoArrays(prev, curr) {
      if (prev) {
        if (curr) {
          return prev.concat(curr);
        }
        return prev;
      }
      return curr;
    }
  }
};
</script>

<style scoped>
.chart {
  height: 80%;
  padding: 20px;
}
</style>
