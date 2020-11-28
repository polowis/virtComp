<template>
    <div>
        <nav class="navbar" role="navigation" aria-label="main navigation">
                    <div class="navbar-brand">
                      <a class="navbar-item" href="/">
                        <img src="/static/img/logo.png" width="112" height="28">
                      </a>
                  
                      <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                      </a>
                    </div>
                  
                    <div id="navbarBasicExample" class="navbar-menu">
                      <div class="navbar-start">
                        <a class="navbar-item" href="/">
                          Home
                        </a>
                  
                        <a class="navbar-item">
                          Documentation
                        </a>
                  
                        <div class="navbar-item has-dropdown is-hoverable">
                          <a class="navbar-link">
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
                  
                      <div class="navbar-end">
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
export default {
    
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