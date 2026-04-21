import React, { useReducer, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Pause, ChevronLeft, ChevronRight, RefreshCw, Palette, Type } from 'lucide-react';
import { reducer, initialState } from './reducer';
import { splitText } from './utils';
import './App.css';

const App: React.FC = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const timerRef = useRef<number | null>(null);
  const lastTimeRef = useRef<number>(0);
  const accumulatedTimeRef = useRef<number>(0);

  const {
    inputText,
    sentences,
    currentIndex,
    isPlaying,
    isInputMode,
    displayMode,
    randomOrder,
    theme,
    fontWeight,
  } = state;

  const currentSentenceIndex = displayMode === 'random' ? randomOrder[currentIndex] : currentIndex;
  const currentSentence = sentences[currentSentenceIndex];

  const handleNext = useCallback(() => {
    dispatch({ type: 'NEXT_SENTENCE' });
    accumulatedTimeRef.current = 0;
  }, []);

  const handlePrev = useCallback(() => {
    dispatch({ type: 'PREV_SENTENCE' });
    accumulatedTimeRef.current = 0;
  }, []);

  const handleTogglePlay = useCallback(() => {
    dispatch({ type: 'TOGGLE_PLAY' });
  }, []);

  const handleStart = () => {
    const splitSentences = splitText(inputText);
    if (splitSentences.length > 0) {
      dispatch({ type: 'START_DISPLAY', payload: splitSentences });
    }
  };

  const handleThemeChange = (newTheme: string) => {
    dispatch({ type: 'SET_THEME', payload: newTheme as any });
  };

  const handleFontWeightChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newWeight = parseInt(e.target.value);
    dispatch({ type: 'SET_FONT_WEIGHT', payload: newWeight });
  };

  // requestAnimationFrame Timer
  useEffect(() => {
    if (!isPlaying || isInputMode || !currentSentence) {
      if (timerRef.current) cancelAnimationFrame(timerRef.current);
      return;
    }

    const animate = (time: number) => {
      if (!lastTimeRef.current) lastTimeRef.current = time;
      const deltaTime = time - lastTimeRef.current;
      lastTimeRef.current = time;

      accumulatedTimeRef.current += deltaTime;

      if (accumulatedTimeRef.current >= currentSentence.duration) {
        handleNext();
      }

      timerRef.current = requestAnimationFrame(animate);
    };

    lastTimeRef.current = performance.now();
    timerRef.current = requestAnimationFrame(animate);

    return () => {
      if (timerRef.current) cancelAnimationFrame(timerRef.current);
    };
  }, [isPlaying, isInputMode, currentSentence, handleNext]);

  // Keyboard Shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (isInputMode) return;

      switch (e.code) {
        case 'Space':
          e.preventDefault();
          handleTogglePlay();
          break;
        case 'ArrowLeft':
          handlePrev();
          break;
        case 'ArrowRight':
          handleNext();
          break;
        case 'KeyR':
          dispatch({ type: 'TOGGLE_MODE' });
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isInputMode, handleTogglePlay, handleNext, handlePrev]);

  return (
    <div className={`app-container theme-${theme}`}>
      <AnimatePresence mode="wait">
        {isInputMode ? (
          <motion.div
            key="input-screen"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="input-screen"
          >
            <textarea
              className="text-input"
              value={inputText}
              onChange={(e) => dispatch({ type: 'SET_INPUT_TEXT', payload: e.target.value })}
              placeholder="在此粘贴或输入您的文本"
            />
            <button className="start-button" onClick={handleStart}>
              开始展示
            </button>
          </motion.div>
        ) : (
          <motion.div
            key="display-screen"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="display-screen"
          >
            <div className="display-area">
              <AnimatePresence mode="wait">
                <motion.div
                  key={currentSentenceIndex}
                  initial={{ y: 40, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: -40, opacity: 0 }}
                  transition={{
                    duration: 0.6,
                    ease: [0.22, 1, 0.36, 1],
                  }}
                  className="sentence-text"
                  style={{ fontWeight: fontWeight }}
                >
                  {currentSentence?.text}
                </motion.div>
              </AnimatePresence>
            </div>

            {/* Pause Overlay */}
            {!isPlaying && (
              <div className="pause-overlay"></div>
            )}

            {/* Toolbar */}
            <div className="toolbar-container">
              <div className="toolbar">
                <button className="tool-btn" onClick={handlePrev} title="上一条">
                  <ChevronLeft size={24} />
                </button>
                <button className="tool-btn play-pause" onClick={handleTogglePlay}>
                  {isPlaying ? <Pause size={24} /> : <Play size={24} />}
                  <span className="btn-text">{isPlaying ? '暂停' : '继续'}</span>
                </button>
                <button className="tool-btn" onClick={handleNext} title="下一条">
                  <ChevronRight size={24} />
                </button>
                <button 
                  className={`tool-btn mode-toggle ${displayMode === 'random' ? 'active' : ''}`} 
                  onClick={() => dispatch({ type: 'TOGGLE_MODE' })}
                  title={displayMode === 'random' ? '随机模式' : '顺序模式'}
                >
                  <RefreshCw size={20} />
                </button>
                <div className="theme-selector">
                  <button className="tool-btn" title="主题选择">
                    <Palette size={20} />
                  </button>
                  <div className="theme-options">
                    <button 
                      className={`theme-option ${theme === 'dark' ? 'active' : ''}`} 
                      onClick={() => handleThemeChange('dark')}
                      title="深色主题"
                    />
                    <button 
                      className={`theme-option ${theme === 'light' ? 'active' : ''}`} 
                      onClick={() => handleThemeChange('light')}
                      title="浅色主题"
                    />
                    <button 
                      className={`theme-option ${theme === 'ocean' ? 'active' : ''}`} 
                      onClick={() => handleThemeChange('ocean')}
                      title="海洋主题"
                    />
                    <button 
                      className={`theme-option ${theme === 'forest' ? 'active' : ''}`} 
                      onClick={() => handleThemeChange('forest')}
                      title="森林主题"
                    />
                    <button 
                      className={`theme-option ${theme === 'sunset' ? 'active' : ''}`} 
                      onClick={() => handleThemeChange('sunset')}
                      title="日落主题"
                    />
                  </div>
                </div>
                <div className="font-weight-control">
                  <button className="tool-btn" title="字体粗细">
                    <Type size={20} />
                  </button>
                  <div className="font-weight-slider-container">
                    <input
                      type="range"
                      min="100"
                      max="900"
                      step="100"
                      value={fontWeight}
                      onChange={handleFontWeightChange}
                      className="font-weight-slider"
                    />
                  </div>
                </div>
                <button className="tool-btn exit-btn" onClick={() => dispatch({ type: 'RESET_INPUT' })}>
                  退出
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default App;
