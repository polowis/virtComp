<template>
    <div>
    <NavbarComponent></NavbarComponent>

    <div class="wrapper-table">
         <div style="width: 700px">
         <a class="button is-primary is-small is-pulled-right">
                <span class="icon is-small">
                <i class="fas fa-redo"></i>
                </span>
                <span @click.prevent="fetchLands()">Refresh</span>
        </a>
        </div>
        <table class="table is-hoverable" style="width: 700px">
            <thead>
                <th>Land ID</th>
                <th>Buy Cost</th>
                <th>Rent Cost</th>
                <th>Level</th>
            </thead>
            <tbody>
                <tr v-for="land in lands" v-bind:key="land.land_id">
                    <td style="cursor: pointer; color: #00d1b2" @click.prevent="redirectToLand(land.land_id)">{{land.land_id}}</td>
                    <td>{{land.buy_cost}}</td>
                    <td>{{land.rent_cost}}</td>
                    <td>{{land.level}}</td>

                </tr>
                <!--
                <tr v-for="company in companiesOwned" v-bind:key=company.company_id>
                    <td @click.prevent="registerSavedCompany(company.company_name)" style="cursor: pointer; color: #00d1b2">{{company.company_name}}</td>
                    <td>{{company.balance}}</td>
                    <td>0</td>
                    <td>0</td>
                </tr>-->
            </tbody>
        </table>
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
            lands: []
        }
    },

    created() {
        this.fetchLands()
    },

    methods: {
        fetchLands() {
            axios.post('/land/view/').then(response => {
                let data = response.data
                if(data.hasOwnProperty('error')){
                    window.location.href = data.redirect_url
                }
                this.lands = data
            })
        },

        shortenLandID(land_id){
            return land_id.substring(0, 10) + '...'
        },

        redirectToLand(land_id) {
            window.location.href = `/land/${land_id}/view/`
        }
    }
}
</script>
<style scoped>
.wrapper-table {
        margin: auto;
        width: 700px;
    }
</style>