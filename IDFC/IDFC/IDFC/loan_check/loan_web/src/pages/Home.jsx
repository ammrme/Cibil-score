import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

import logo from "../assets/idf-logo.png";
import personal from "../assets/IDFC.png";
import home from "../assets/house.jpg";
import business from "../assets/bussiness.jpg";

function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    if (!window.gsap) return;

    const tl = window.gsap.timeline();

    tl.to(".logo", { opacity: 1, y: -10, duration: 0.8 })
      .to(".headline", { opacity: 1, y: -10, duration: 0.8 })
      .to(".card", {
        opacity: 1,
        y: 0,
        stagger: 0.2,
        duration: 0.6,
        ease: "power2.out",
      })
      .to(".steps", { opacity: 1, duration: 0.5 })
      .to(".cta", { opacity: 1, scale: 1.05, duration: 0.4 });
  }, []);

  return (
    <section className="hero">
      {/* LOGO */}
      <img src={logo} className="logo" alt="IDFC First Bank Logo" />

      {/* HEADLINE */}
      <h1 className="headline">Instant Loans. Zero Hassle.</h1>

      {/* CARDS */}
      <div className="cards">
        <div className="card">
          <div className="image-box">
            <img
              src={personal}
              className="card-img"
              alt="Personal Loan"
            />
          </div>
          <span>Personal Loan</span>
        </div>

        <div className="card">
          <div className="image-box">
            <img
              src={home}
              className="card-img"
              alt="Home Loan"
            />
          </div>
          <span>Home Loan</span>
        </div>

        <div className="card">
          <div className="image-box">
            <img
              src={business}
              className="card-img"
              alt="Business Loan"
            />
          </div>
          <span>Business Loan</span>
        </div>
      </div>

      {/* STEPS */}
      <div className="steps">
        Apply → Verify → Approve → Disburse
      </div>

      {/* CTA */}
      <button className="cta" onClick={() => navigate("/check-score")}>
        Check Score
      </button>
    </section>
  );
}

export default Home;
