import React, { useState } from "react"
import { Link } from "react-router-dom"
import "./Header.css"

const Navbar = () => {
  // Toogle Menu
  const [MobileMenu, setMobileMenu] = useState(false)
  return (
    <>
      <header className='header'>
        <div className='container c_flex'>
          {/* <div className='catgrories d_flex'>
            <span class='fa-solid fa-border-all'></span>
            <h4>
              Dashboard
            </h4>
          </div> */}
          <div className='logo width '>
            {/* <img src={logo} alt='' /> */}
            <h2 style={{color: "purple", fontSize: "30px"}}><i class="fab fa-linode fa-pulse fa-lg"></i> FirNOW</h2>
          </div>
        
          <div className='navlink'>
            <ul className={MobileMenu ? "nav-links-MobileMenu" : "link f_flex capitalize"} onClick={() => setMobileMenu(false)} >
              {/*<ul className='link f_flex uppercase {MobileMenu ? "nav-links-MobileMenu" : "nav-links"} onClick={() => setMobileMenu(false)}'>*/}
              <li>
                <Link to='/'>Home</Link>
              </li>
              {/* <li>
                <Link to='/news'>News</Link>
              </li> */}
              <li>
                <Link to='/police-station/dashboard'>Dashboard</Link>
              </li>
              {/* <li>
                <Link to='/whyus'>Why Us</Link>
              </li> */}
              <li>
                <Link to='/lodgeFir'>Lodge Fir</Link>
              </li>
              <li>
                 <Link to='/police-station/register'>
                 <button className="Nav_Reg">
                     Register
                  </button>
                 </Link>
              </li>
              <li>
                 <Link to='/login'>
                 <button className="Nav_Reg">
                     Login
                  </button>
                 </Link>
              </li>
            </ul>

            <button className='toggle' onClick={() => setMobileMenu(!MobileMenu)}>
              {MobileMenu ? <i className='fas fa-times close home-btn'></i> : <i className='fas fa-bars open'></i>}
            </button>
          </div>
        </div>
      </header>
    </>
  )
}

export default Navbar
