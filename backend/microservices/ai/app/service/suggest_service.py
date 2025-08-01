from typing import List

from fastapi import HTTPException

from app.requests.adoption_mcrsrv import get_animals_descriptions

import logging

from app.schema.pet_desc_dto import PetDescDTO

from transformers import pipeline

from app.schema.user_suggest_dto import UserSuggestDTO

logger = logging.getLogger(__name__)

class SuggestService:
    async def process_profile_created_suggestion(self, message_body: dict):
        logger.info("Starting to process suggestions based on desc...")


        user: UserSuggestDTO = UserSuggestDTO(**message_body)
        logger.info(f"USER_DATA_FOR_SUGGEST {user}")

        try:
            pets_desc: List[PetDescDTO] = await get_animals_descriptions(latitude=user.latitude, longitude=user.longitude)
        except HTTPException as e:
            logger.error(f"HTTP Exception while processing suggestions for: {user}")
            return
        logger.info(f"Retrieved pets desc {pets_desc}")
        #
        # # person_bio = [
        # #     "A 28-year-old fitness enthusiast who loves trail running, mountain biking, and outdoor adventures. Passionate about staying active every day and exploring new hiking routes."
        # # ]
        # person_bio = [
        #     "A 40-year-old who prefers relaxing at home, enjoys watching movies, and rarely goes for walks. Values comfort and peaceful downtime."
        # ]
        # person_bio = [
        #     "26 year old software developer, spending my time mostly inside. I like to take walks in the park with my girlfriends dog, but not everyday. My social batteries are not too high, so im not very active socially."
        # ]
        #
        # person_bio = [
        #     "24 year old psychologist, love being outside and meeting people. I like walking and being active, always doing something. At the end of the day i still have energy."
        # ]
        # animal_bios = [
        #         "This person has a personality similar to a friendly dog, always excited to greet everyone.",
        #         "This person has a personality similar to a sleepy cat, lounging around all day without a care.",
        #         "This person has a personality similar to a colorful parrot, constantly chatting and mimicking sounds.",
        #         "This person has a personality similar to a playful rabbit, hopping around with boundless energy.",
        #         "This person has a personality similar to a loyal dog, sticking close to its favorite person.",
        #         "This person has a personality similar to a curious kitten, exploring every corner of the house.",
        #         "This person has a personality similar to a noisy parrot, never missing a chance to make some noise.",
        #         "This person has a personality similar to a gentle guinea pig, quietly nibbling on fresh veggies.",
        #         "This person has a personality similar to a fluffy hamster, always running on its wheel for fun.",
        #         "This person has a personality similar to a calm dog, patiently waiting for a belly rub.",
        #         "This person has a personality similar to a stubborn goat, always doing things their own way.",
        #         "This person has a personality similar to a cuddly cat, purring contently in cozy spots.",
        #         "This person has a personality similar to a clever parrot, picking up new things quickly.",
        #         "This person has a personality similar to a tiny mouse, quiet but always alert.",
        #         "This person has a personality similar to a chubby pug, lovable and full of charm.",
        #         "This person has a personality similar to a relaxed turtle, taking life one slow step at a time.",
        #         "This person has a personality similar to an eager puppy, full of enthusiasm and energy.",
        #         "This person has a personality similar to a proud peacock, always showing off a little flair.",
        #         "This person has a personality similar to a gentle dove, calm and peaceful in every setting.",
        #         "This person has a personality similar to a bouncy ferret, always exploring tight spaces.",
        #         "This person has a personality similar to a cheerful canary, singing from morning till night.",
        #         "This person has a personality similar to a snuggly bunny, soft and full of warmth.",
        #         "This person has a personality similar to a sleepy hedgehog, rolled up in a cozy ball.",
        #         "This person has a personality similar to a watchful cat, always observing from a distance.",
        #         "This person has a personality similar to a playful Labrador, ready for games at any time.",
        #         "This person has a personality similar to a sassy Siamese cat, never shy to express opinions.",
        #         "This person has a personality similar to a giggly parakeet, chirping in short bursts of joy.",
        #         "This person has a personality similar to a calm goldfish, floating peacefully in its own world.",
        #         "This person has a personality similar to a helpful sheepdog, always ready to assist others.",
        #         "This person has a personality similar to a tiny chick, following others with trust and curiosity."
        # ]
        #
        # classifier = pipeline("zero-shot-classification",
        #                       model="facebook/bart-large-mnli")
        #
        # sequence_to_classify = person_bio[0]
        # import time
        # start_time = time.time()
        # classif_result = classifier(sequence_to_classify, animal_bios, multi_label=True)
        # logger.info(f"IT TOOK {time.time() - start_time}s to classify {len(animal_bios)} bios.")
        #
        # for label, score in zip(classif_result.get('labels'), classif_result.get('scores')):
        #     logger.info(f"SCORE: {score}\nSENTENCE: {label}")