<template>
    <div>
    <NavbarComponent></NavbarComponent>
    <div class="page">
        <div class="app-content">
            <div class="wrapper-table">
                <h1 style="float:left; width: 30%; color: #54ff5f; margin-left: 10%;">Your lands</h1>
                <h1 style="float:right; width: 30%; color: #f02929">Lands on sale </h1>
                <div style="width:85%; float:right;">
                    
                    <a class="button is-primary is-small is-pulled-right">
                    <span class="icon is-small">
                        <i class="fas fa-redo"></i>
                    </span>
                    <span @click.prevent="fetchLands()">Refresh</span>
                </a>
                </div>
                <table class="table is-hoverable is-pulled-left" style="width: 40%; color: #ffffff">
                    <thead>
                        <th>Land ID</th>
                        <th>Level</th>
                        <th>Continent</th>
                    </thead>
                    <tbody>
                        <tr v-for="land in this.landsOwned" v-bind:key="land.land_id" class="hover-row">
                            <td style="cursor: pointer; color: #00d1b2"><a :href="'/land/' + land.land_id + '/view/'" style="color: #00d1b2">{{land.land_id}}</a></td>
                            <td>{{land.level}}</td>
                            <td>{{land.continent}}</td>
                        </tr>
                    </tbody>
                </table>
                <table class="table is-hoverable is-pulled-right" style="width: 40%; color: #ffffff">
                    <thead>
                        <th>Land ID</th>
                        <th>Buy Cost</th>
                        <th>Rent Cost</th>
                        <th>Continent</th>
                    </thead>
                    <tbody>
                        <tr v-for="land in this.normalizeLandData()" v-bind:key="land.land_id" class="hover-row">
                            <td style="cursor: pointer; color: #00d1b2"><a :href="'/land/' + land.land_id + '/view/'" style="color: #00d1b2">{{land.land_id}}</a></td>
                            <td><i class="fas fa-caret-up" style="color:#00ff00"></i> ${{land.buy_cost}}</td>
                            <td>${{land.rent_cost}}</td>
                            <td>{{land.continent}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    </div>
</template>
<script>
import NavbarComponent from '../../NavbarComponent'
export default {
    components: {
        NavbarComponent
    },

    data() {
        return {
            lands: [],
            landsOwned: []
        }
    },

    mounted() {
        this.fetchLands()
        this.fetchOwnedLands()
    },

    computed: {
        
    },

    methods: {
        fetchLands() {
            axios.get('/api/v1/landscape/browse/').then(response => {
                let data = response.data
                if(data.hasOwnProperty('error')){
                    window.location.href = data.redirect_url
                }
                this.lands = data
            })
        },

        fetchOwnedLands() {
            axios.get('/api/v1/landscape/').then(response => {
                let data = response.data
                this.landsOwned = data
            })
        },

        shortenLandID(land_id){
            return land_id.substring(0, 10) + '...'
        },

        titleCase(str) {
            let splitString = str.toLowerCase().split(' ');
            for (let i = 0; i < splitString.length; i++) {
                // You do not need to check if i is larger than splitStr length, as your for does that for you
                // Assign it back to the array
                splitString[i] = splitString[i].charAt(0).toUpperCase() + splitString[i].substring(1);     
            }
            // Directly return the joined string
            return splitString.join(' '); 
        },

        normalizeLandData() {
            return this.lands.map(land =>{
                let tempLand = Object.assign({}, land)
                tempLand.continent = this.titleCase(land.continent)
                return tempLand

            })
        }

    }
}
</script>
<style scoped>
.wrapper-table {
        margin: auto;
        width: 95%;
    }
.table thead th{
    color: #03a9f4 !important;
    font-size: 10px;
}

.hover-row:hover{
    background-color:  #3a4441 !important;
}
</style>