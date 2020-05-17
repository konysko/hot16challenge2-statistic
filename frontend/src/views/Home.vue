<template>
  <div class="wrapper">
    <section class="section">
      <div class="sectionHeader">
        <h2 class="sectionTitle">Zebrana kwota z utworami na YouTube</h2>
        <v-switch v-model="isDateRange" @change="onChangeIsDateRange" color="#de4000" label="Wykres dzienny"></v-switch>
      </div>
      <v-menu
        v-if="isDateRange"
        v-model="dateMenu"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            color="#272727"
            v-model="date"
            label="Wykres dla dnia"
            readonly
            v-on="on"
            outlined
          ></v-text-field>
        </template>
        <v-date-picker color="#272727" v-model="date" @change="onChangeDate" @input="dateMenu = false"></v-date-picker>
      </v-menu>
      <icon-chart
        v-if="loaded"
        :chart-total-amount-values="chartTotalAmountValuesOnDay"
        :chart-video-values="chartVideoOnDay"
        :chart-labels="dataLabelsOnDay"
      ></icon-chart>
    </section>
    <section class="section">
      <h2 class="sectionTitle">Zebrana kwota i skumulowana liczba utworów na YouTube</h2>
      <v-select
        color="#272727"
        item-color="#272727"
        :items="ranges"
        v-model="range"
        @change="onChangeRange"
        label="Zakres kumulacji"
        outlined
      ></v-select>
      <line-chart
        v-if="loaded"
        :chart-total-amount-values="chartTotalAmountValues"
        :chart-video-count-values="chartVideoCountValues"
        :chart-labels="dataLabels"
      ></line-chart>
    </section>
  </div>
</template>

<script>
import moment from 'moment';

import IconChart from '@/components/IconChart.vue';
import LineChart from '@/components/LineChart.vue';

export default {
  name: 'Home',
  components: {
    IconChart,
    LineChart
  },
  data() {
    return {
      statistic: null,
      chartTotalAmountValues: null,
      chartVideoCountValues: null,
      chartTotalAmountValuesOnDay: null,
      chartVideoOnDay: null,
      dataLabelsOnDay: null,
      loaded: false,
      ranges: ['Godzina', 'Dzień'],
      range: 'Dzień',
      isDateRange: false,
      date: new Date(2019, 4, 2).toISOString().substr(0, 10),
      dateMenu: false
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
      this.setStatisticChartDataDay(this.statistic, this.date, this.isDateRange);

      this.loaded = true;
    },
    setStatisticChartData(statistic, range) {
      const rangedStatistic = this.getRangesStatistic(statistic, range);

      this.chartTotalAmountValues = rangedStatistic.map((timeSlot) => timeSlot.total_sum_amount);
      this.chartVideoCountValues = rangedStatistic.map((timeSlot) => {
        const videoTitles = timeSlot.video_titles;
        return videoTitles ? videoTitles.length : 0;
      });
      this.dataLabels = rangedStatistic.map((timeSlot) =>
        range === 'Godzina' ? moment(timeSlot.date).format('MM-DD   HH:mm') : moment(timeSlot.date).format('MM-DD')
      );
    },
    setStatisticChartDataDay(statistic, date, isDateRange) {
      const statisticForDay = isDateRange ? this.getStatisticForDate(statistic, date) : statistic;
      const yearStartDay = moment(`${Number(moment(statistic[0].date).format('YYYY'))}-01-01`);

      this.chartTotalAmountValuesOnDay = statisticForDay.map((timeSlot) => {
        const hoursFromStart = moment(timeSlot.date).diff(yearStartDay, 'hours');
        const currHour = hoursFromStart;
        return {
          x: currHour,
          y: timeSlot.total_sum_amount
        };
      });
      this.chartVideoOnDay = statisticForDay.reduce((prevArr, curr) => {
        const hoursFromStart = moment(curr.date).diff(yearStartDay, 'hours');
        const currHour = hoursFromStart;
        if (curr.video_titles) {
          curr.video_titles.forEach((value, idx) =>
            prevArr.push({
              x: currHour,
              y: idx,
              yLabel: value,
              r: isDateRange ? 15 : 5,
              video_title: value,
              video_url: curr.video_urls[idx],
              video_thumbnail: curr.video_thumbnails[idx]
            })
          );
        }
        return prevArr;
      }, []);
      this.dataLabelsOnDay = statisticForDay.map((timeSlot) =>
        isDateRange ? moment(timeSlot.date).format('HH:mm') : moment(timeSlot.date).format('MM-DD   HH:mm')
      );
    },
    onChangeRange(range) {
      this.setStatisticChartData(this.statistic, range);
    },
    onChangeDate(date) {
      this.setStatisticChartDataDay(this.statistic, date, this.isDateRange);
    },
    onChangeIsDateRange(isDateRange) {
      this.setStatisticChartDataDay(this.statistic, this.date, isDateRange);
    },
    getRangesStatistic(statistic, range) {
      if (range === 'Godzina') {
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
    getStatisticForDate(statistic, date) {
      return statistic.filter((item) => moment(item.date).format('YYYY-MM-DD') === date);
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
.wrapper {
  height: 80%;
  padding: 40px 20px;
}
.section {
  margin-bottom: 60px;
}
.sectionHeader {
  display: flex;
  justify-content: space-between;
}
.sectionTitle {
  margin: 10px 0 20px 0;
}
</style>
