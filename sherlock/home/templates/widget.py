CROSS_SELL_WIDGET_HTML_TEMPLATE = """
    window['{{ widget_callback }}'](
        `
        <link rel="stylesheet" href="https://sherlockfr.s3.eu-west-3.amazonaws.com/widget.css" media="all" />
        
        <div
            id="sherlock-section-{{ environment }}"
            style="
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding-bottom: 5px;
                border: 1px solid #d9d9d9;
                border-radius: 5px;
                margin-top: 1em;
                padding: 1.8em 16px 1rem;
                background-color: #fff;
                color: #333;
                font-weight: 500;
            "
        >
            <h1 class="widget__title">{{ widget_title }}</h1>
            {% if widget_description %}
            <p class="widget__subtitle">
                {{ widget_description }}
            </p>
            {% endif %} 
            <hr size="1" width="100%" color="#d9d9d9" />

            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@splidejs/splide@latest/dist/css/splide.min.css" />
            <style>
                .underline-hover:hover {
                    text-decoration: underline;
                }
                .cross-price {
                    text-decoration: none;
                    position: relative;
                    font-size: 12px;
                }
                .cross-price::before {
                    content: "";
                    width: 100%;
                    position: absolute;
                    right: 0;
                    top: 40%;
                    border-bottom: 1px solid rgb(0, 0, 0);
                }
                .link-style {
                    color: black;
                }
                .my-carousel-progress {
                    background: #ccc;
                    width: 30%;
                    margin: auto;
                }

                .my-carousel-progress-bar-1 {
                    background: #7dc1ff;
                    height: 2px;
                    transition: width 400ms ease;
                    width: 0;
                }
                .my-carousel-progress-bar-2 {
                    background: #7dc1ff;
                    height: 2px;
                    transition: width 400ms ease;
                    width: 0;
                }
            </style>

            <div id="sherlock-splide" class="splide">
                <div class="splide__track" style="margin: 10px 15px;">
                    <div class="splide__list">
                        {% for product in products %}
                        <a class="splide__slide link-style" href="{{ product.visit_url }}" target="_blank">
                            <img class="widget__store-carousel__contents__content__card__image" src="{{ product.image_url }}" />
                            <div class="widget__store-carousel__contents__content__card__info">
                                <p style="min-width: 100%;" class="widget__store-carousel__contents__content__card__info__title">
                                    {{ product.title }}
                                </p>
                                <div class="widget__store-carousel__contents__content__card__info__prices">
                                    <p class="widget__store-carousel__contents__content__card__info__prices__new-price">
                                        €{{ product.price }}
                                    </p>
                                </div>
                                <div class="widget__store-carousel__contents__content__card__info__external-link">
                                    <p class="widget__store-carousel__contents__content__card__info__external-link__text">
                                        Voir
                                    </p>
                                    <img class="widget__store-carousel__contents__content__card__info__external-link__icon" src="https://sherlockfr.s3.eu-west-3.amazonaws.com/images/arrow-right-icon.svg" />
                                </div>
                            </div>
                        </a>
                        {% endfor %}
                    </div>
                </div>
                <!-- Add the progress bar element -->
                <div class="my-carousel-progress">
                    <div class="my-carousel-progress-bar"></div>
                </div>
            </div>

        </div>
        `
    )
"""
