import React from "react"
import "./style.css"

const Wrapper = () => {
  const data = [
    {
      cover: <i class="fa-brands fa-ethereum"></i>,
      title: "Web3 based",
      decs: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    },
    {
      cover: <i class='fa-solid fa-id-card'></i>,
      title: "Safety of victim",
      decs: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    },
    {
      cover: <i class='fa-solid fa-shield'></i>,
      title: "Secure your info ",
      decs: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    },
    {
      cover: <i class='fa-solid fa-headset'></i>,
      title: "24/7 Support ",
      decs: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    },
  ]
  return (
    <>
      <section className='wrapper background'>
        <div className='container grid2'>
          {data.map((val, index) => {
            return (
              <div className='product' key={index}>
                <div className='img icon-circle'>
                  <i>{val.cover}</i>
                </div>
                <h3>{val.title}</h3>
                <p>{val.decs}</p>
              </div>
            )
          })}
        </div>
      </section>
    </>
  )
}

export default Wrapper
