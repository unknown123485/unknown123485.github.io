import { Sentence } from './types';

export const splitText = (text: string): Sentence[] => {
  // Split by paragraphs first
  const paragraphs = text.split(/\n\n+/);
  const sentences: Sentence[] = [];

  paragraphs.forEach((para) => {
    // Split by Chinese/English punctuation: 。 . ? !
    const splitRegex = /([^。！？.?!]+[。！？.?!]?)/g;
    const matches = para.match(splitRegex);

    if (matches) {
      matches.forEach((s) => {
        const trimmed = s.trim();
        if (trimmed) {
          // duration = max(2s, 0.4s * charCount), rounded to 0.1s
          const charCount = trimmed.length;
          const durationSec = Math.max(2, 0.4 * charCount);
          const roundedDuration = Math.floor(durationSec * 10) / 10;
          
          sentences.push({
            text: trimmed,
            duration: roundedDuration * 1000, // convert to ms
          });
        }
      });
    } else if (para.trim()) {
      // If no punctuation but has text
      const trimmed = para.trim();
      const charCount = trimmed.length;
      const durationSec = Math.max(2, 0.4 * charCount);
      const roundedDuration = Math.floor(durationSec * 10) / 10;
      sentences.push({
        text: trimmed,
        duration: roundedDuration * 1000,
      });
    }
  });

  return sentences;
};

export const shuffleArray = (array: number[]): number[] => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};
