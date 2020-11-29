<template>
    <div>
        <NavbarComponent></NavbarComponent>
                

            <div class="form">
            <h3 id="form-header">Register</h3>
            <div class="field">
                    <label class="label">Username</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="text" placeholder="Username" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-user"></i>
                      </span>
                    </div>
            </div>
            <div class="field">
                    <label class="label">Email</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="email" placeholder="Email Address" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-envelope"></i>
                      </span>
                    </div>
            </div>

            <div class="field">
                    <label class="label">Password</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="password" placeholder="" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-key"></i>
                      </span>
                    </div>
            </div>

            <div class="field">
                    <label class="label">Repeat password</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="password" placeholder="" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-eye-slash"></i>
                      </span>
                    </div>
            </div>

            <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox">
                        I agree to the <a href="/terms">terms and conditions</a>
                      </label>
                    </div>
            </div>

            <div class="control">
                    <button class="button is-primary">Submit</button>
            </div>
        </div>
    </div>
</template>
<script>
import NavbarComponent from '../NavbarComponent'
export default {
    components: {
        NavbarComponent
    },

    data() {
        return {
            username: "",
            email: ""
        }
    },

    watch: {
        username: function() {
            this.debounceUsername()
        }
    },

    created() {
        this.debounceUsername = _debounce(this.checkUsernameAvaibility, 50)
    },

    methods: {
        checkUsernameAvaibility() {
            if(this.username.length > 0) {
                let form = new FormData()
                form.append("username", this.username)

                axios.post('/user/isavailable', form, { headers: {
                'Content-Type': 'multipart/form-data'
                }}).then(response => {
                    let data = response.data
                })
            }
        }
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
        #form-header {
            text-align: center;
            text-transform:uppercase;
            font-weight: bold;
            font-size: 30px;
        }
</style>