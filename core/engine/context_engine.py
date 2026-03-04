"""
N-Gram Context Engine for AdorLipi.

Tracks the previous word and uses Bengali bigram pairs to disambiguate
the current word. For example, if the previous word is 'নদীর', then
'ধারে' should be boosted over 'দারে'.
"""

class ContextEngine:
    def __init__(self):
        self.prev_word = None
        
        # Bengali bigram pairs: (prev_word_prefix, current_word)
        # If the previous committed word STARTS WITH the prefix,
        # the current_word gets a boost in suggestions.
        # Format: { 'prev_prefix': ['boosted_word1', 'boosted_word2'] }
        self.bigrams = {
            # Nature collocations
            'নদী': ['ধারে', 'পারে', 'তীরে', 'জলে', 'স্রোতে'],
            'আকাশ': ['নীল', 'মেঘ', 'তারা', 'জুড়ে', 'থেকে'],
            'বৃষ্টি': ['ভেজা', 'পড়ে', 'থামে', 'নামে', 'হচ্ছে'],
            'ফুল': ['ফুটে', 'ফোটে', 'গন্ধ', 'বাগান', 'সুবাস'],
            'পাখি': ['ডাকে', 'উড়ে', 'গান', 'বসে'],
            'সাগর': ['তীরে', 'পারে', 'জলে', 'ঢেউ'],
            'চাঁদ': ['আলো', 'রাত', 'উঠে', 'ওঠে'],
            'সূর্য': ['ওঠে', 'অস্ত', 'আলো', 'রশ্মি'],
            'শীত': ['কুয়াশা', 'ঠান্ডা', 'সকাল', 'রাত'],
            'গরম': ['দিন', 'আবহাওয়া', 'পানি'],
            
            # Emotion collocations
            'ভালো': ['লাগে', 'বাসি', 'থাকো', 'আছি', 'হবে', 'মানুষ'],
            'খারাপ': ['লাগে', 'হয়ে', 'সময়', 'খবর', 'দিন'],
            'মন': ['খারাপ', 'ভালো', 'চায়', 'কাঁদে', 'মানে'],
            'চোখ': ['জল', 'মুছে', 'দিয়ে', 'ভরা', 'মেলে'],
            'হৃদয়': ['ভেঙে', 'মাঝে', 'দিয়ে', 'গভীরে'],
            'কষ্ট': ['পাই', 'হয়', 'দিও', 'করো', 'সব'],
            'স্বপ্ন': ['দেখি', 'দেখে', 'ভেঙে', 'পূরণ'],
            'প্রেম': ['হয়ে', 'করে', 'ভালোবাসা', 'গল্প'],
            
            # Action collocations
            'কথা': ['বলো', 'বলে', 'শুনো', 'শুনে', 'দাও', 'হয়'],
            'গান': ['শুনি', 'গাই', 'শুনো', 'গেয়ে', 'ভালো'],
            'কাজ': ['করো', 'করে', 'করি', 'হয়ে', 'শেষ'],
            'খাবার': ['খেয়ে', 'রান্না', 'ভালো', 'দাও'],
            'পড়া': ['শেষ', 'করো', 'লেখা', 'বই'],
            
            # Grammar context
            'আমি': ['তোমাকে', 'তোমায়', 'যাবো', 'করবো', 'চাই', 'জানি', 'ভালোবাসি'],
            'তুমি': ['আমাকে', 'আমায়', 'যাবে', 'করবে', 'জানো', 'এসো'],
            'আমার': ['মন', 'কথা', 'জীবন', 'ভালো', 'সোনা', 'প্রিয়'],
            'তোমার': ['জন্য', 'কাছে', 'সাথে', 'হাত', 'চোখ'],
            'সে': ['বলে', 'যায়', 'আসে', 'জানে', 'চায়'],
            'যদি': ['আবার', 'তুমি', 'কখনো', 'একদিন'],
            'কেন': ['বলো', 'যাও', 'করো', 'এমন'],
            'কিন্তু': ['আমি', 'তুমি', 'সে', 'এটা', 'তবু'],
            
            # Time collocations
            'আজ': ['রাতে', 'সকালে', 'দুপুরে', 'আবার', 'থেকে'],
            'কাল': ['রাতে', 'সকালে', 'থেকে', 'আসবে', 'যাবো'],
            'রাত': ['শেষ', 'হয়ে', 'জেগে', 'গভীর', 'পোহালো'],
            'সকাল': ['বেলা', 'হলো', 'থেকে', 'সন্ধ্যা'],
            'দিন': ['রাত', 'যায়', 'কাটে', 'শেষ', 'এমন'],
            
            # Possessive context
            'সবার': ['জন্য', 'মাঝে', 'সাথে', 'কাছে'],
            'এই': ['গান', 'কথা', 'পথ', 'দিন', 'রাত', 'জীবন'],
            'সেই': ['দিন', 'রাত', 'মানুষ', 'সময়', 'কথা'],
        }

    def set_context(self, committed_bangla_word):
        """Called after each word is committed to track context."""
        if committed_bangla_word:
            self.prev_word = committed_bangla_word.strip()

    def clear_context(self):
        """Called when the user resets or starts a new sentence."""
        self.prev_word = None

    def get_boosted_words(self):
        """
        Returns a list of Bangla words that should be boosted in the
        suggestion list given the previous word context.
        """
        if not self.prev_word:
            return []

        boosted = []
        for prefix, words in self.bigrams.items():
            if self.prev_word.startswith(prefix):
                boosted.extend(words)

        return boosted

    def score_boost(self, word):
        """
        Returns a boost score for a word based on n-gram context.
        Higher = more likely given the previous word.
        """
        boosted = self.get_boosted_words()
        if not boosted:
            return 0

        for boost_word in boosted:
            if word.startswith(boost_word) or word == boost_word:
                return 50  # Strong context boost

        return 0
