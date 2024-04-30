import React from "react"
import Sdata from "./Sdata"
import Slider from "react-slick"
import "slick-carousel/slick/slick.css"
import "slick-carousel/slick/slick-theme.css"

const SlideCard = () => {
  const settings = {
    dots: false,
    infinite: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    appendDots: (dots) => {
      return <ul style={{ margin: "0px" }}>{dots}</ul>
    },
  }
  return (
    <>
      <Slider {...settings}>
        {Sdata.map((value, index) => {
          return (
            <>
              <div className='box d_flex top' key={index}>
                <div className='left'>
                  <h1 className="title">{value.title}</h1>
                  <p className="title">{value.desc}</p>
                  <br/>
                  <button className='btn-primary'>Explore More</button>
                </div>

                <div className='right img-slide-animation'>
                  <img className="slideCover" src={value.cover} alt='' />
                </div>
                
              </div>
              <br/>
              <br/>
            </>
          )
        })}
        
      </Slider>
      <br/>
      <br/>
    </>
  )
}

export default SlideCard
