<template>
    <div>
        <NavbarComponent></NavbarComponent>
        <div class="form">
            <div class="field">
                    <label class="label">Name</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input is-primary" type="text" placeholder="Company's name" v-model="companyName" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-building"></i>
                      </span>
                    </div>
                    <div v-if="companyAvailability == true" style="color: #00d1b2">The company name is available to register</div>
                    <div v-if="companyAvailability == false" style="color: #e60c0c">The company name is not available</div>
            </div>

            

            <div class="control">
                    <button class="button is-primary">Submit</button>
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
            companyName: "",
            companyAvailability: false
        }
    },

    watch: {
        companyName: function() {
            this.debounceGetCompanyName()
        }
    },

    created() {
        this.debounceGetCompanyName = _.debounce(this.checkAvailableCompany, 50)
    },

    methods: {
        checkAvailableCompany() {
            let form = new FormData()
            form.append("companyName", this.companyName)
            axios.post('/company/hasavailablename/', form, { headers: {
                'Content-Type': 'multipart/form-data'
                }}).then(response=> {
                    let data = response.data
                    this.companyAvailability = data.available
            })
        },

    }
}
</script>

<style scoped>
.form {
    margin:3% auto 0 auto;
    padding:30px;
    width:400px;
    height:auto;
    overflow:hidden;
    background:white;
    border-radius:10px;
}
</style>