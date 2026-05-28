package com.masreader.app.ui.theme

import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.ReadOnlyComposable
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.ui.graphics.Color
import com.masreader.app.data.model.AppTheme
import com.masreader.app.data.model.ThemeColorRegistry
import com.masreader.app.data.model.ThemeColors

// Strict monochrome palette for e-ink. Provided app-wide so EVERY screen
// that reads themeColors.accent / textPrimary / bgBase automatically
// renders pure black-on-white (no orange/purple bleed-through).
val EInkThemeColors = ThemeColors(
    bgBase = Color.White,
    textPrimary = Color.Black,
    accent = Color.Black,
    bgGradientCenter = Color.White,
    bgGradientEnd = Color.White,
    matrixBgColor = Color.White,
    matrixCharColor = Color.Black,
    matrixCharTail = Color.Black,
    isDark = false,
    isEInk = true
)

fun eInkThemeColors(variant: String): ThemeColors = when (variant) {
    "archive" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFFFFFF),
        textPrimary = Color(0xFF050505),
        accent = Color(0xFF050505),
        bgGradientCenter = Color(0xFFFFFFFF),
        bgGradientEnd = Color(0xFFF3F3F3),
        matrixBgColor = Color(0xFFFFFFFF),
        matrixCharColor = Color(0xFF050505),
        matrixCharTail = Color(0xFF555555),
        defaultFontWeight = 500
    )
    "paper" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFAF7ED),
        textPrimary = Color(0xFF17140F),
        accent = Color(0xFF17140F),
        bgGradientCenter = Color(0xFFFAF7ED),
        bgGradientEnd = Color(0xFFECE5D2),
        matrixBgColor = Color(0xFFFAF7ED),
        matrixCharColor = Color(0xFF17140F),
        matrixCharTail = Color(0xFF635D4F),
        hasPaperTexture = true
    )
    "graphite" -> EInkThemeColors.copy(
        bgBase = Color(0xFFF2F3F1),
        textPrimary = Color(0xFF0D0F0E),
        accent = Color(0xFF0D0F0E),
        bgGradientCenter = Color(0xFFF2F3F1),
        bgGradientEnd = Color(0xFFD8DDDA),
        matrixBgColor = Color(0xFFF2F3F1),
        matrixCharColor = Color(0xFF0D0F0E),
        matrixCharTail = Color(0xFF4B504E)
    )
    "marginalia" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFFFEFA),
        textPrimary = Color(0xFF000000),
        accent = Color(0xFF000000),
        bgGradientCenter = Color(0xFFFFFEFA),
        bgGradientEnd = Color(0xFFF0F0ED),
        matrixBgColor = Color(0xFFFFFEFA),
        matrixCharColor = Color(0xFF000000),
        matrixCharTail = Color(0xFF303030),
        defaultFontWeight = 450
    )
    "suzu" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFAFAF5),
        textPrimary = Color(0xFF1A1A1A),
        accent = Color(0xFF8A7E6E),
        bgGradientCenter = Color(0xFFFAFAF5),
        bgGradientEnd = Color(0xFFEDE8DC),
        matrixBgColor = Color(0xFFFAFAF5),
        matrixCharColor = Color(0xFF1A1A1A),
        matrixCharTail = Color(0xFF7A7A7A),
        hasPaperTexture = true,
        defaultFontWeight = 400,
        letterSpacing = 0.05f
    )
    "moke" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFFFFFF),
        textPrimary = Color(0xFF000000),
        accent = Color(0xFF000000),
        bgGradientCenter = Color(0xFFFFFFFF),
        bgGradientEnd = Color(0xFFFFFFFF),
        matrixBgColor = Color(0xFFFFFFFF),
        matrixCharColor = Color(0xFF000000),
        matrixCharTail = Color(0xFF000000),
        defaultFontWeight = 500
    )
    "letterpress" -> EInkThemeColors.copy(
        bgBase = Color(0xFFF8F6F0),
        textPrimary = Color(0xFF1C1C1C),
        accent = Color(0xFF5C5C5C),
        bgGradientCenter = Color(0xFFF8F6F0),
        bgGradientEnd = Color(0xFFE8E4DC),
        matrixBgColor = Color(0xFFF8F6F0),
        matrixCharColor = Color(0xFF1C1C1C),
        matrixCharTail = Color(0xFF8A7E6E),
        hasPaperTexture = true
    )
    "zhujian" -> EInkThemeColors.copy(
        bgBase = Color(0xFFF7F3ED),
        textPrimary = Color(0xFF2A2018),
        accent = Color(0xFF8B2500),
        bgGradientCenter = Color(0xFFF7F3ED),
        bgGradientEnd = Color(0xFFEDE8DC),
        matrixBgColor = Color(0xFFF7F3ED),
        matrixCharColor = Color(0xFF2A2018),
        matrixCharTail = Color(0xFF8B7355),
        hasPaperTexture = true
    )
    "blueprint" -> EInkThemeColors.copy(
        bgBase = Color(0xFFF5F5F0),
        textPrimary = Color(0xFF2A2A2A),
        accent = Color(0xFF1A3A5A),
        bgGradientCenter = Color(0xFFF5F5F0),
        bgGradientEnd = Color(0xFFE0E8F0),
        matrixBgColor = Color(0xFFF5F5F0),
        matrixCharColor = Color(0xFF2A2A2A),
        matrixCharTail = Color(0xFF6A6A6A)
    )
    "flow" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFDFDF8),
        textPrimary = Color(0xFF1A1A1A),
        accent = Color(0xFF4A4A4A),
        bgGradientCenter = Color(0xFFFDFDF8),
        bgGradientEnd = Color(0xFFF0EDE6),
        matrixBgColor = Color(0xFFFDFDF8),
        matrixCharColor = Color(0xFF1A1A1A),
        matrixCharTail = Color(0xFF8A8A8A)
    )
    "movabletype" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFAFAFA),
        textPrimary = Color(0xFF0A0A0A),
        accent = Color(0xFF0A0A0A),
        bgGradientCenter = Color(0xFFFAFAFA),
        bgGradientEnd = Color(0xFFEAEAEA),
        matrixBgColor = Color(0xFFFAFAFA),
        matrixCharColor = Color(0xFF0A0A0A),
        matrixCharTail = Color(0xFF3A3A3A),
        defaultFontWeight = 500
    )
    "cardindex" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFFFEF5),
        textPrimary = Color(0xFF2C2C2C),
        accent = Color(0xFF5C5040),
        bgGradientCenter = Color(0xFFFFFEF5),
        bgGradientEnd = Color(0xFFF5F0E0),
        matrixBgColor = Color(0xFFFFFEF5),
        matrixCharColor = Color(0xFF2C2C2C),
        matrixCharTail = Color(0xFF8A8070)
    )
    "zenink" -> EInkThemeColors.copy(
        bgBase = Color(0xFFFEFEFE),
        textPrimary = Color(0xFF1A1A1A),
        accent = Color(0xFF1A1A1A),
        bgGradientCenter = Color(0xFFFEFEFE),
        bgGradientEnd = Color(0xFFF4F4F4),
        matrixBgColor = Color(0xFFFEFEFE),
        matrixCharColor = Color(0xFF1A1A1A),
        matrixCharTail = Color(0xFF8A8A8A)
    )
    "terminal" -> EInkThemeColors.copy(
        bgBase = Color(0xFF0A0A0A),
        textPrimary = Color(0xFFE0E0E0),
        accent = Color(0xFFE0E0E0),
        bgGradientCenter = Color(0xFF0A0A0A),
        bgGradientEnd = Color(0xFF1A1A1A),
        matrixBgColor = Color(0xFF0A0A0A),
        matrixCharColor = Color(0xFFE0E0E0),
        matrixCharTail = Color(0xFF555555),
        isDark = true,
        defaultFontWeight = 500
    )
    else -> EInkThemeColors
}

val LocalThemeColors = compositionLocalOf<ThemeColors> {
    ThemeColorRegistry.get(AppTheme.MYSTIC)
}

/** Global e-ink mode flag. Any composable can read it to render mono-only UI. */
val LocalEInk = compositionLocalOf { false }

/** Global low-performance mode flag. When ON, composables that read it should
 *  skip expensive per-frame work (drawBackdrop shaders, blur, lens, matrix
 *  rain, infinite animations, etc.) and render a cheap static equivalent.
 *  Unlike e-ink, the app's colours and layouts are preserved — only GPU-
 *  heavy effects are bypassed. Most users leave this OFF, so the normal
 *  visual effects must stay untouched when it's off. */
val LocalLowPerf = compositionLocalOf { false }

object MasReaderTheme {
    val colors: ThemeColors
        @Composable
        @ReadOnlyComposable
        get() = LocalThemeColors.current
}

@Composable
fun MasReaderTheme(
    theme: AppTheme = AppTheme.MYSTIC,
    eInk: Boolean = false,
    eInkVariant: String = "classic",
    content: @Composable () -> Unit
) {
    // In e-ink mode hand the WHOLE app a monochrome palette so colour
    // can't leak through anywhere.
    val themeColors = if (eInk) eInkThemeColors(eInkVariant) else ThemeColorRegistry.get(theme)
    CompositionLocalProvider(
        LocalThemeColors provides themeColors,
        LocalEInk provides eInk,
        content = content
    )
}
