<template>
    <div>
        <NavbarComponent></NavbarComponent>
                

            <div class="form">
            <h3 id="form-header">Register</h3>
            <div class="field">
                    <label class="label">Username</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="text" placeholder="Username" v-model="username" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-user"></i>
                      </span>
                    </div>
            </div>
            <div class="field">
                    <label class="label">Email</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="email" placeholder="Email Address" v-model="email" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-envelope"></i>
                      </span>
                    </div>
            </div>

            <div class="field">
                <div v-if="credentialAvailability == true && username.length > 0 && email.length > 0" style="color: #00d1b2">Username and email are valid</div>
            </div>

            <div class="field">
                <div v-if="credentialAvailability == false && username.length > 0 && email.length > 0" style="color: #e60c0c">Username or email is invalid</div>
            </div>

            <div class="field">
                    <label class="label">Password</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="password" v-model="password" placeholder="" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-key"></i>
                      </span>
                    </div>
            </div>

            <div class="field">
                    <label class="label">Repeat password</label>
                    <div class="control has-icons-left has-icons-right">
                      <input class="input" type="password" v-model="repeatPassword" placeholder="" value="">
                      <span class="icon is-small is-left">
                        <i class="fas fa-eye-slash"></i>
                      </span>
                    </div>
            </div>
            <div class="field">
                <div v-if="repeatPasswordIsMatched()" style="color: #00d1b2">Password matched</div>
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
                    <button class="button is-primary" @click.prevent="register()">Submit</button>
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
            email: "",
            password: "",
            repeatPassword: "",
            credentialAvailability: false,
            passwordLength: false
        }
    },

    watch: {
        username: function() {
            this.debounceUsername()
        },

        email: function() {
            this.debounceEmail()
        },

        password: function() {
            this.debouncePassword()
        },

        repeatPassword: function() {
            this.debounceRepeatPassword()
        }
    },

    created() {
        this.debounceUsername = _.debounce(this.checkAvaibility, 50)
        this.debounceEmail = _.debounce(this.checkAvaibility, 50)
        this.debouncePassword = _.debounce(this.checkPassword, 50)
        this.debounceRepeatPassword = _.debounce(this.checkPassword, 50)
    },

    methods: {
        checkAvaibility() {
            if(this.username.length > 0 && this.email.length > 0) {
                let form = new FormData()
                form.append("username", this.username)
                form.append('email', this.email)

                axios.post('/user/isavailable/', form, { headers: {
                    'Content-Type': 'multipart/form-data'
                }}).then(response => {
                    let data = response.data
                    this.credentialAvailability = data.available
                })
            }
        },

        checkUsernameAvaibility() {
            if(this.username.length > 0 && this.email.length > 0) {
                let form = new FormData()
                form.append("username", this.username)

                axios.post('/user/isavailable/', form, { headers: {
                    'Content-Type': 'multipart/form-data'
                }}).then(response => {
                    let data = response.data
                    this.credentialAvailability = data.available
                })
            }
        },

        checkEmailAvailability() {
            if(this.username.length > 0 && this.email.length > 0) {
                let form = new FormData()
                form.append("email", this.email)

                axios.post('/user/isavailable/', form, { headers: {
                    'Content-Type': 'multipart/form-data'
                }}).then(response => {
                    let data = response.data
                    this.credentialAvailability = data.available
                })
            }
        },

        repeatPasswordIsMatched() {
            if(this.password.length > 7 && this.repeatPassword.length > 7) {
                return this.password == this.repeatPassword
            }

        },

        checkPassword() {
            if(this.password.length > 0 && this.password.length < 8) {
                this.passwordLength = true
            }

            if(this.password.length > 0 && this.password.length > 7) {
                this.passwordLength = false
            }
        },

        register() {
            if(this.credentialAvailability && this.passwordLength) {
                let form = new FormData()
                form.append('username', this.username)
                form.append('email', this.email)
                form.append('password', this.password)
                form.append('repeatPassword', this.repeatPassword)

                axios.post('/register/', form, { headers: {'Content-Type': 'multipart/form-data'}}).then(response => {
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