export function Navbar() {
    return (
        <nav class="navigation_18 bg-dark pt-30 pb-30 lh-40 text-center">
            <div class="container px-xl-0">
                <div class="row justify-content-between align-items-center">
                    <div class="col-lg-auto text-lg-left" data-aos-duration="600" data-aos="fade-down" data-aos-delay="0">
                        <a href="#" class="logo link color-white">InfiniBot</a>
                    </div>
                    <div class="col-lg-9 text-lg-right" data-aos-duration="600" data-aos="fade-down" data-aos-delay="300">
                        <a href="#" class="link color-white mr-15">Documentation</a>
                        <a href="https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands" class="link color-white mx-15">Invite</a>
                        <a href="./about.html" class="link color-white mx-15">About</a>
                        <a href="#" class="link color-white mx-15">F.A.Q.</a>
                        <a href="./support.html" class="link color-white mx-15">Support</a>
                        <a href="./terms.html" class="link color-white mx-15">Terms of Service</a>
                        <a href="https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands" class="mt-45 btn lg action-1" style="margin-top: -10px; margin-left: 50px;">Dashboard</a>
                        {/* <form method="GET" action="/" class="ml-15 mt-10 mt-md-0 d-inline-block">
					<input type="text" name="search" placeholder="Search" class="input sm w-200 mw-full border-transparent-white focus-white color-white placeholder-transparent-white text-center text-md-left" />
					<input type="submit" class="d-none" />
				</form> */}
                    </div>
                </div>
            </div>
        </nav>
    )
}