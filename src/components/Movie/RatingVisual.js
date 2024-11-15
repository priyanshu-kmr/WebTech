// components/RatingVisual/RatingVisual.js
import React from 'react';
import '../../css/RatingVisual.css';

const RatingVisual = ({ rating }) => {
    const filledStars = Math.round(rating);
    const emptyStars = 5 - filledStars;

    return (
        <div className="rating-visual" title={`Rating: ${rating}`}>
            {Array(filledStars).fill().map((_, i) => (
                <span key={i} className="star filled">★</span>
            ))}
            {Array(emptyStars).fill().map((_, i) => (
                <span key={i} className="star empty">☆</span>
            ))}
        </div>
    );
};

export default RatingVisual;