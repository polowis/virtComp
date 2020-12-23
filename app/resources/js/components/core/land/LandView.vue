<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="page">
            <div class="app-content">
                <div class="land-photo">
                    <figure class="image">
                    <img src="/static/img/land.png" class="land-image">
                    </figure>
                    </div>
                <div class="land-details">
                    <h3>Land ID: {{land.land_id}}</h3>
                    
                    <p>Company Owner: {{land.company_name}}</p>
                    <p v-if="land.company_name !== null">Land Status: Not available to purchase </p>
                    <p v-else style="color: #00d1b2">Land Status: Available to purchase</p>
                    <p>Land Level: {{land.level}}</p>
                    <p>Land Cost: ${{land.buy_cost}}</p>
                    <p>Land Rent: ${{land.rent_cost}} / week</p>
                    <p>Land Continent: {{this.titleCase(land.continent)}}</p>
                    <p v-if="land.company_name === null" style="color: #00d1b2">Available to buy/rent</p>
                    <div v-if="land.company_name === null">
                        <div class="control">
                            <button class="button is-primary" @click.prevent="confirmedBuy = true">Buy</button>
                            <button class="button is-primary" @click.prevent="confirmedRent = true">Rent</button>
                        </div>
                        <div class="control" v-if="confirmedBuy" style="margin-top: 20px">
                            <button class="button is-dark" @click.prevent="buyLand()">Confirm Buy</button>
                            <button class="button is-danger" @click.prevent="confirmedBuy = false">Cancel</button>
                        </div>
                        <div class="control" v-if="confirmedRent" style="margin-top: 20px">
                            <button class="button is-dark" @click.prevent="rentLand()">Confirm Rent</button>
                            <button class="button is-danger" @click.prevent="confirmedRent = false">Cancel</button>
                        </div>
                    </div>
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
            land: "",
            confirmedBuy: false,
            confirmedRent: false
        }
    },

    created() {
        this.fetchLandDetail()
    },

    methods: {
        fetchLandDetail() {
            axios.post((location.pathname+location.search)).then(response => {
                let data = response.data
                this.land = data
            })
        },

        buyLand() {
            axios.post(`/land/${this.land.land_id}/buy`).then(response => {

            })
        },

        titleCase(str="asia") {
            let splitString = str.toLowerCase().split(' ');
            for (let i = 0; i < splitString.length; i++) {
               
                splitString[i] = splitString[i].charAt(0).toUpperCase() + splitString[i].substring(1);     
            }
            return splitString.join(' '); 
        },

    }

}
</script>

<style scoped>
.land-photo {
    width: 500px;
    float: left;
    margin-left: 20px;
}

.land-details{
    width: 500px;
    float:right;
    margin-right: 20px;
}
.land-image{
    width: 500px; 
    height: 300px
}
</style>