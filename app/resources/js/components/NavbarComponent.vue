<template>
    <div>
        <nav class="navbar" role="navigation" aria-label="main navigation">
                    <div class="navbar-brand">
                      <a class="navbar-item" href="/">
                        <img src="/static/img/logo.png" width="112" height="28">
                      </a>
                  
                      <a role="button" class="navbar-burger burger" style="color:white" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                      </a>
                    </div>
                  
                    <div id="navbarBasicExample" class="navbar-menu">
                      <div class="navbar-start">
                        <a class="navbar-item" href="/home/" style="color:white">
                          Home
                        </a>
                  
                        <a class="navbar-item" href="#" style="color:white">
                          Documentation
                        </a>
                  
                        <div class="navbar-item has-dropdown is-hoverable">
                          <a class="navbar-link" style="color:white;">
                            More
                          </a>
                  
                          <div class="navbar-dropdown">
                            <a class="navbar-item">
                              About
                            </a>
                            <a class="navbar-item">
                              Jobs
                            </a>
                            <a class="navbar-item">
                              Contact
                            </a>
                            <hr class="navbar-divider">
                            <a class="navbar-item">
                              Report an issue
                            </a>
                          </div>
                        </div>
                      </div>
                    
                    <div class="navbar-end" v-if="user.id != 'none'">
                        <div class="navbar-item">
                            <div class="buttons">
                                
                                <a class="button is-primary">Hi {{this.user.username}}</a>
                                <a class="button is-danger" @click.prevent="logout()">
                                    <strong>Log out</strong>
                                </a>
                            </div>
                        </div>
                     </div>

                      <div class="navbar-end" v-if="user.id == 'none'">
                        <div class="navbar-item">
                          <div class="buttons">
                            <a class="button is-primary" href="/register">
                              <strong>Sign up</strong>
                            </a>
                            <a class="button is-light" href="/login">
                              Log in
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </nav>
    </div>
</template>
<script>
export default {
    data() {
        return {
            user: ""
        }
    },

    created(){
        this.getCurrentUser()

    },
    methods: {
        getCurrentUser() {
            axios.get("/user/current/").then(response =>{
                let data = response.data
                this.user = data
            })
        },

        logout() {
            axios.post('/logout/').then(response =>{
              let data = response.data
              if(data.message == 'success') {
                window.location = data.redirect_url
              }
            })
        }
    }
}
</script>
<style scoped>
.navbar {
  background-color: #63736e;
}

.navbar-item {
  background-color: #63736e;
  color: white;
}

a.navbar-item:hover{
  background-color: #3a4441;
}

a.navbar-link:hover{
  background-color: #3a4441;
}
.navbar-menu {
  background-color: #63736e;
}

.navbar-link {
  color: #f9ffcb;
}

.navbar-dropdown {
  background-color: #63736e;
  border-top: 1px solid #63736e;
}

.navbar-divider {
   background-color: #63736e;
}

.has-dropdown{
  background-color: #63736e;
}
</style>