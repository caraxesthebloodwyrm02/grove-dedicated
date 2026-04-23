sky = "blue"
sun = "bright"
clouds = "fluffy"


def make_story(current_sky, current_sun, current_clouds):
    if current_sun == "bright":
        return (
            "The "
            f"{current_sun} sun stretched across the {current_sky} sky,"
            f" inviting the {current_clouds} clouds to drift lazily. "
            "Children traced shapes in the gentle fluff while the warm glow"
            " painted everything with morning hope."
        )
    else:
        return (
            "The shy sun hid for a moment, letting the "
            f"{current_clouds} clouds whisper across the {current_sky} canvas."
        )


def main():
    story = make_story(sky, sun, clouds)
    print(story)


if __name__ == "__main__":
    main()
