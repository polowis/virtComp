<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="page">
            <div class="app-content">
                <div class="wrapper-table">
                <table class="table is-hoverable" style="width: 700px; color: #ffffff">
                <thead>
                    <th>Land ID</th>
                    <th>Buy Cost</th>
                    <th>Rent Cost</th>
                    <th>Level</th>
                    <th>Continent</th>
                </thead>
            <tbody>
                <tr v-for="land in this.lands" v-bind:key="land.land_id" class="hover-row">
                    <td style="cursor: pointer; color: #00d1b2"><a :href="'/land/' + land.land_id + '/view/'" style="color: #00d1b2">{{land.land_id}}</a></td>
                    <td v-if="land.is_rent">${{land.rent_cost}}</td>
                    <td>{{land.level}}</td>
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

import NavbarComponent from '../../../NavbarComponent'
export default {
    components: {
        NavbarComponent
    },

    data() {
        return {
            lands: []
        }
    },

    mounted() {
        this.fetchCompanyLand()
    },

    methods: {
        fetchCompanyLand() {
            axios.post('/company/land/all/').then(response => {
                let data = response.data
                this.lands = data
            })
        }
    }
}
</script>
<style scoped>
.wrapper-table {
        margin: auto;
        width: 700px;
    }
.table thead th{
    color: #03a9f4 !important;
}

.hover-row:hover{
    background-color:  #3a4441 !important;
}
</style>