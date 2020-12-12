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
                    <p>Land Status: {{land.status}}</p>
                    <p>Land Level: {{land.level}}</p>
                    <p>Land Cost: {{land.buy_cost}}</p>
                    <p>Land Rent: {{land.rent_cost}}</p>
                    <p v-if="land.company_name === null" style="color: #00d1b2">Available to buy/rent</p>
                    <div v-if="land.company_name === null">
                        <div class="control">
                            <button class="button is-primary" @click.prevent="buyLand()">Buy</button>
                            <button class="button is-primary" @click.prevent="rentLand()">Rent</button>
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
            land: ""
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
        }
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