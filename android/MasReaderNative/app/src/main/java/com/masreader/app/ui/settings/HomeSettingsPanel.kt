package com.masreader.app.ui.settings

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.*
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.*
import androidx.lifecycle.viewmodel.compose.viewModel
import com.masreader.app.data.model.AppTheme
import com.masreader.app.data.model.BackgroundEffect
import com.masreader.app.data.model.ThemeColorRegistry
import com.masreader.app.data.model.ThemeColors
import com.masreader.app.ui.theme.LocalEInk
import com.masreader.app.ui.theme.LocalThemeColors
import kotlin.math.abs
import kotlinx.coroutines.launch

@Composable
fun HomeSettingsPanel(
    viewModel: HomeSettingsViewModel = viewModel(),
    onDismiss: () -> Unit
) {
    val settings by viewModel.settings.collectAsState()
    val themeColors = LocalThemeColors.current
    val eInk = LocalEInk.current

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
            .background(themeColors.bgBase.copy(alpha = 0.97f))
            .navigationBarsPadding()
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 12.dp, bottom = 4.dp),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .width(36.dp).height(4.dp)
                    .clip(CircleShape)
                    .background(themeColors.textPrimary.copy(alpha = 0.25f))
            )
        }

        if (!eInk) {
            CollapsibleSliderGroup(
                title = "主题选择",
                themeColors = themeColors,
                persistKey = "home_theme_group"
            ) {
                ThemeSelectorDial(
                    currentTheme = settings.homeTheme,
                    onThemeChanged = { viewModel.updateTheme(it) }
                )
            }
            Spacer(Modifier.height(8.dp))
        }

        if (eInk) {
            SettingsSectionTitle("墨水屏主题", themeColors)
            EInkThemeSelector(
                current = settings.eInkThemeVariant,
                themeColors = themeColors,
                onSelect = { key -> viewModel.update { copy(eInkThemeVariant = key) } }
            )
        } else {
            SettingsSectionTitle("背景特效", themeColors)
            BackgroundEffectSelector(
                current = settings.backgroundEffect,
                themeColors = themeColors,
                onSelect = { viewModel.updateBackgroundEffect(it) }
            )
        }

        Spacer(Modifier.height(8.dp))

        // ── Silent Archive 档案样式(增量,默认 off — 不动现有界面) ──
        SettingsSectionTitle("档案样式 · Silent Archive", themeColors)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 6.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            listOf(
                "off" to "关闭",
                "archive" to "静默档案",
                "paper" to "仿纸张"
            ).forEach { (key, label) ->
                val sel = settings.archiveStyleVariant == key
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(50))
                        .background(
                            if (sel) themeColors.accent.copy(alpha = 0.25f)
                            else themeColors.textPrimary.copy(alpha = 0.06f)
                        )
                        .clickable { viewModel.update { copy(archiveStyleVariant = key) } }
                        .padding(vertical = 9.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        label,
                        color = if (sel) themeColors.accent
                        else themeColors.textPrimary.copy(alpha = 0.65f),
                        fontSize = 12.sp,
                        fontWeight = if (sel) FontWeight.SemiBold else FontWeight.Normal
                    )
                }
            }
        }
        Text(
            "开启后,书库列表 + 阅读器顶/底栏 + 章节扉页会切换成档案册式排版。",
            color = themeColors.textPrimary.copy(alpha = 0.45f),
            fontSize = 11.sp,
            modifier = Modifier.padding(horizontal = 20.dp, vertical = 4.dp)
        )

        Spacer(Modifier.height(12.dp))

        // ── 导入/导出设置(全 app HomeSettings + ReadingSettings) ──
        SettingsSectionTitle("导入/导出设置", themeColors)
        ImportExportSection(themeColors)

        Spacer(Modifier.height(8.dp))

        // ── 界面缩放 (DPI) ──
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp, vertical = 4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                "界面缩放",
                color = themeColors.textPrimary.copy(alpha = 0.45f),
                fontSize = 11.sp,
                fontWeight = FontWeight.Medium,
                letterSpacing = 0.8.sp,
                modifier = Modifier.weight(1f)
            )
            Text(
                "${(settings.uiDpiScale * 100).toInt()}%",
                color = themeColors.accent,
                fontSize = 12.sp,
                fontWeight = FontWeight.SemiBold
            )
        }
        androidx.compose.material3.Slider(
            value = settings.uiDpiScale,
            onValueChange = { viewModel.updateUiDpiScale(it) },
            valueRange = 0.8f..1.4f,
            steps = 11,
            colors = androidx.compose.material3.SliderDefaults.colors(
                thumbColor = themeColors.accent,
                activeTrackColor = themeColors.accent,
                inactiveTrackColor = themeColors.textPrimary.copy(alpha = 0.18f)
            ),
            modifier = Modifier.padding(horizontal = 16.dp)
        )

        Spacer(Modifier.height(16.dp))
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  ThemeSelectorDial — 3-row vertical drum
//
//  Two thin horizontal lines (accent color, 30 % alpha) frame the center row,
//  plus a 3dp left accent bar. No border box. Classic iOS picker aesthetic.
// ─────────────────────────────────────────────────────────────────────────────

@Composable
private fun EInkThemeSelector(
    current: String,
    themeColors: ThemeColors,
    onSelect: (String) -> Unit
) {
    val options = listOf(
        "classic" to "经典高对比",
        "archive" to "静默档案",
        "paper" to "旧纸阅读",
        "graphite" to "石墨卡片",
        "marginalia" to "边注学报",
        "suzu" to "素笺",
        "moke" to "墨刻",
        "letterpress" to "铅印",
        "zhujian" to "竹简",
        "blueprint" to "蓝图",
        "flow" to "流",
        "movabletype" to "活字",
        "cardindex" to "卡片",
        "zenink" to "禅墨",
        "terminal" to "终端"
    )
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        options.chunked(2).forEach { row ->
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                row.forEach { (key, label) ->
                    val selected = current == key
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .height(42.dp)
                            .clip(RoundedCornerShape(12.dp))
                            .background(
                                if (selected) themeColors.textPrimary.copy(alpha = 0.14f)
                                else themeColors.textPrimary.copy(alpha = 0.04f)
                            )
                            .border(
                                1.dp,
                                if (selected) themeColors.textPrimary
                                else themeColors.textPrimary.copy(alpha = 0.24f),
                                RoundedCornerShape(12.dp)
                            )
                            .clickable { onSelect(key) },
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            label,
                            color = themeColors.textPrimary,
                            fontSize = 12.sp,
                            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Normal,
                            textAlign = TextAlign.Center
                        )
                    }
                }
                if (row.size == 1) Spacer(Modifier.weight(1f))
            }
        }
    }
}

private val DRUM_H    = 48.dp
private const val DRUM_ROWS = 3

@Composable
fun ThemeSelectorDial(
    currentTheme: AppTheme,
    onThemeChanged: (AppTheme) -> Unit
) {
    val themeColors = LocalThemeColors.current
    val themes      = remember { AppTheme.entries.toList() }
    val listState   = rememberLazyListState()
    val fling       = rememberSnapFlingBehavior(listState)

    val initIdx = remember(currentTheme) { themes.indexOf(currentTheme).coerceAtLeast(0) }
    LaunchedEffect(Unit) { listState.scrollToItem(initIdx) }

    val centeredIdx by remember {
        derivedStateOf {
            val info = listState.layoutInfo
            val mid  = info.viewportStartOffset + info.viewportSize.height / 2
            info.visibleItemsInfo.minByOrNull { abs((it.offset + it.size / 2) - mid) }?.index
                ?: initIdx
        }
    }
    LaunchedEffect(centeredIdx) {
        if (centeredIdx in themes.indices) onThemeChanged(themes[centeredIdx])
    }

    val drumHeight = DRUM_H * DRUM_ROWS
    val sidePad    = (drumHeight - DRUM_H) / 2   // = DRUM_H

    Column(modifier = Modifier.fillMaxWidth()) {

        // Header — live theme name on the right
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                "配色方案",
                color         = themeColors.textPrimary.copy(alpha = 0.45f),
                fontSize      = 11.sp,
                fontWeight    = FontWeight.Medium,
                letterSpacing = 0.8.sp,
                modifier      = Modifier.weight(1f)
            )
            Text(
                themes.getOrNull(centeredIdx)?.displayName ?: "",
                color      = themeColors.accent,
                fontSize   = 12.sp,
                fontWeight = FontWeight.SemiBold
            )
        }

        // ── Theme preview card ─────────────────────────────────────────────
        HomeThemePreview(
            theme       = themes.getOrNull(centeredIdx) ?: currentTheme,
            themeColors = themeColors
        )

        Spacer(Modifier.height(8.dp))

        Box(modifier = Modifier.fillMaxWidth().height(drumHeight)) {

            // ── Scrollable rows ────────────────────────────────────────────
            LazyColumn(
                state          = listState,
                flingBehavior  = fling,
                contentPadding = PaddingValues(vertical = sidePad),
                modifier       = Modifier.fillMaxSize()
            ) {
                itemsIndexed(themes) { index, theme ->
                    HomeDrumRow(
                        theme          = theme,
                        distFromCenter = index - centeredIdx,
                        themeColors    = themeColors,
                        height         = DRUM_H
                    )
                }
            }

            // ── Top / bottom fade ──────────────────────────────────────────
            Box(
                modifier = Modifier
                    .fillMaxWidth().height(sidePad).align(Alignment.TopCenter)
                    .background(Brush.verticalGradient(
                        listOf(themeColors.bgBase.copy(alpha = 0.62f), Color.Transparent)
                    ))
            )
            Box(
                modifier = Modifier
                    .fillMaxWidth().height(sidePad).align(Alignment.BottomCenter)
                    .background(Brush.verticalGradient(
                        listOf(Color.Transparent, themeColors.bgBase.copy(alpha = 0.62f))
                    ))
            )
        }

        Spacer(Modifier.height(4.dp))
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  HomeDrumRow
// ─────────────────────────────────────────────────────────────────────────────

@Composable
private fun HomeDrumRow(
    theme: AppTheme,
    distFromCenter: Int,
    themeColors: ThemeColors,
    height: Dp
) {
    val colors  = ThemeColorRegistry.get(theme)
    val absDist = abs(distFromCenter)

    val highlightAlpha by animateFloatAsState(
        targetValue   = if (absDist == 0) 1f else 0f,
        animationSpec = tween(220, easing = FastOutSlowInEasing),
        label         = "highlight"
    )
    val contentAlpha by animateFloatAsState(
        targetValue   = when (absDist) { 0 -> 1.00f; 1 -> 0.38f; else -> 0.14f },
        animationSpec = tween(160),
        label         = "content"
    )
    val swatchDp by animateFloatAsState(
        targetValue   = when (absDist) { 0 -> 22f; else -> 13f },
        animationSpec = spring(dampingRatio = 0.72f, stiffness = Spring.StiffnessMedium),
        label         = "swatch"
    )

    Box(modifier = Modifier.fillMaxWidth().height(height)) {

        // Center emphasis WITHOUT a rounded box — the old inset rounded
        // rect + border produced the visible "倒角" the user dislikes.
        // Cornerless: a faint full-bleed accent wash + a slim left
        // accent bar, only on the focused row.
        if (highlightAlpha > 0.01f) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .fillMaxHeight()
                    .background(colors.accent.copy(alpha = 0.10f * highlightAlpha))
            )
            Box(
                modifier = Modifier
                    .align(Alignment.CenterStart)
                    .padding(start = 6.dp)
                    .width(3.dp)
                    .fillMaxHeight(0.46f)
                    .background(colors.accent.copy(alpha = 0.85f * highlightAlpha))
            )
        }

        Row(
            modifier = Modifier
                .fillMaxSize()
                .graphicsLayer { alpha = contentAlpha }
                .padding(start = 22.dp, end = 16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // Two-tone swatch: outer ring = theme BACKGROUND color (so
            // dark vs light themes are obvious), inner dot = accent.
            Box(
                modifier = Modifier
                    .size(swatchDp.dp)
                    .clip(CircleShape)
                    .background(colors.bgBase)
                    .border(
                        1.dp,
                        Color.White.copy(alpha = if (absDist == 0) 0.45f else 0.08f),
                        CircleShape
                    ),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier
                        .size((swatchDp * 0.56f).dp)
                        .clip(CircleShape)
                        .background(colors.accent)
                )
            }
            Text(
                text       = theme.displayName,
                color      = if (absDist == 0) colors.accent else themeColors.textPrimary,
                fontSize   = if (absDist == 0) 14.sp else 13.sp,
                fontWeight = if (absDist == 0) FontWeight.SemiBold else FontWeight.Normal,
                maxLines   = 1,
                overflow   = TextOverflow.Ellipsis
            )
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  HomeThemePreview — animated preview card for the selected theme
// ─────────────────────────────────────────────────────────────────────────────

@Composable
private fun HomeThemePreview(theme: AppTheme, themeColors: ThemeColors) {
    val colors = ThemeColorRegistry.get(theme)
    val accentColor by animateColorAsState(colors.accent,      tween(380), label = "pvAccent")
    val textColor   by animateColorAsState(colors.textPrimary, tween(380), label = "pvText")
    val bgColor     by animateColorAsState(colors.bgBase,      tween(380), label = "pvBg")

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(76.dp)
            .padding(horizontal = 10.dp)
            .clip(RoundedCornerShape(14.dp))
            .background(accentColor.copy(alpha = 0.18f))
            .border(1.dp, accentColor.copy(alpha = 0.35f), RoundedCornerShape(14.dp))
    ) {
        Row(
            modifier = Modifier.fillMaxSize().padding(horizontal = 20.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(32.dp)
                    .clip(CircleShape)
                    .background(accentColor)
                    .border(1.dp, Color.White.copy(alpha = 0.45f), CircleShape)
            )
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    "实时预览",
                    color         = textColor.copy(alpha = 0.55f),
                    fontSize      = 10.sp,
                    fontWeight    = FontWeight.Medium,
                    letterSpacing = 0.8.sp
                )
                Spacer(Modifier.height(2.dp))
                Text(
                    text       = theme.displayName,
                    color      = accentColor,
                    fontSize   = 16.sp,
                    fontWeight = FontWeight.SemiBold,
                    maxLines   = 1,
                    overflow   = TextOverflow.Ellipsis
                )
            }
            Column(
                verticalArrangement = Arrangement.spacedBy(4.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Box(Modifier.size(10.dp).clip(CircleShape).background(bgColor)
                    .border(0.5.dp, Color.White.copy(alpha = 0.25f), CircleShape))
                Box(Modifier.size(10.dp).clip(CircleShape).background(textColor)
                    .border(0.5.dp, Color.White.copy(alpha = 0.25f), CircleShape))
            }
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
//  BackgroundEffectSelector
// ─────────────────────────────────────────────────────────────────────────────

@Composable
private fun BackgroundEffectSelector(
    current: BackgroundEffect,
    themeColors: ThemeColors,
    onSelect: (BackgroundEffect) -> Unit
) {
    val rows = BackgroundEffect.entries.chunked(4)
    Column(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        rows.forEach { row ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                row.forEach { effect ->
                    val sel = effect == current
                    Surface(
                        onClick = { onSelect(effect) },
                        shape   = RoundedCornerShape(20.dp),
                        color   = if (sel) themeColors.accent.copy(alpha = 0.22f)
                                  else themeColors.textPrimary.copy(alpha = 0.07f),
                        border  = if (sel) BorderStroke(1.dp, themeColors.accent) else null,
                        modifier = Modifier.weight(1f)
                    ) {
                        Text(
                            text     = effect.displayName,
                            color    = if (sel) themeColors.accent
                                       else themeColors.textPrimary.copy(alpha = 0.65f),
                            fontSize = 11.sp,
                            textAlign = TextAlign.Center,
                            modifier  = Modifier.padding(vertical = 7.dp)
                        )
                    }
                }
                repeat(4 - row.size) { Spacer(Modifier.weight(1f)) }
            }
        }
    }
}

@Composable
private fun SettingsSectionTitle(title: String, themeColors: ThemeColors) {
    Text(
        text       = title,
        color      = themeColors.textPrimary.copy(alpha = 0.45f),
        fontSize   = 11.sp,
        fontWeight = FontWeight.Medium,
        letterSpacing = 0.8.sp,
        modifier   = Modifier.padding(horizontal = 20.dp, vertical = 6.dp)
    )
}


/* ��������������������������������������������������������������������������������������������������������������������������������������������
 *  ImportExportSection �� ȫ app ���õ��뵼��
 *  ���ı���(MR.{base64}.v1)�� HomeSettings + ReadingSettings ֮��ת��
 *  - ����: һ�����Ƶ�������
 *  - ����: ճ���� + �㵼��,��������һ����ԭ
 *  �������������������������������������������������������������������������������������������������������������������������������������������� */
@Composable
private fun ImportExportSection(themeColors: ThemeColors) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val app = com.masreader.app.MasReaderApp.instance
    val home by app.settingsDataStore.homeSettings
        .collectAsState(initial = com.masreader.app.data.model.HomeSettings())
    val reading by app.settingsDataStore.readingSettings
        .collectAsState(initial = com.masreader.app.data.model.ReadingSettings())
    val scope = androidx.compose.runtime.rememberCoroutineScope()
    var exportedCode by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
    var importInput by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
    var statusMsg by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // ����ť:����+���� / ճ��+����
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .height(42.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(themeColors.accent.copy(alpha = 0.25f))
                    .border(1.dp, themeColors.accent.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
                    .clickable {
                        val code = com.masreader.app.data.SettingsCodec.encodeAll(context, home, reading)
                        exportedCode = code
                        // �Զ����Ƶ�������
                        val cm = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE)
                            as? android.content.ClipboardManager
                        cm?.setPrimaryClip(android.content.ClipData.newPlainText("mas-reader-settings", code))
                        statusMsg = "�ѵ��� + ���Ƶ�������"
                    },
                contentAlignment = Alignment.Center
            ) {
                Text(
                    "���� + ����",
                    color = themeColors.accent,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }
            Box(
                modifier = Modifier
                    .weight(1f)
                    .height(42.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(themeColors.textPrimary.copy(alpha = 0.10f))
                    .border(1.dp, themeColors.textPrimary.copy(alpha = 0.30f), RoundedCornerShape(12.dp))
                    .clickable {
                        // 1) ������ճ���������
                        // 2) ��Ϊ�����Զ�������
                        val raw = importInput.ifBlank {
                            val cm = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE)
                                as? android.content.ClipboardManager
                            cm?.primaryClip?.getItemAt(0)?.text?.toString().orEmpty()
                        }
                        if (raw.isBlank()) {
                            statusMsg = "ճ����Ϊ���Ҽ�����û����"
                            return@clickable
                        }
                        val decoded = com.masreader.app.data.SettingsCodec.decodeAll(raw)
                        if (decoded == null) {
                            statusMsg = "�벻��,�޷�ʶ��(�� MR. ��ͷ������Ч������)"
                            return@clickable
                        }
                        scope.launch {
                            app.settingsDataStore.saveHomeSettings(decoded.home)
                            app.settingsDataStore.saveReadingSettings(decoded.reading)
                            com.masreader.app.data.SettingsCodec.applyExtraPreferences(context, decoded.prefs)
                            statusMsg = "����ɹ�"
                        }
                    },
                contentAlignment = Alignment.Center
            ) {
                Text(
                    "����",
                    color = themeColors.textPrimary,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }
        }
        // ��������ʾ��
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(78.dp)
                .clip(RoundedCornerShape(10.dp))
                .background(themeColors.textPrimary.copy(alpha = 0.06f))
                .border(0.8.dp, themeColors.textPrimary.copy(alpha = 0.20f), RoundedCornerShape(10.dp))
                .padding(10.dp)
        ) {
            Text(
                exportedCode.ifBlank { "�㡸���� + ���ơ�����������,ճ�����˴����ɵ���" },
                color = themeColors.textPrimary.copy(
                    alpha = if (exportedCode.isBlank()) 0.40f else 0.90f
                ),
                fontSize = 10.sp,
                lineHeight = 13.sp,
                fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                maxLines = 5,
                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
            )
        }
        // ճ����
        androidx.compose.foundation.text.BasicTextField(
            value = importInput,
            onValueChange = { importInput = it },
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp)
                .clip(RoundedCornerShape(10.dp))
                .background(themeColors.textPrimary.copy(alpha = 0.06f))
                .border(0.8.dp, themeColors.textPrimary.copy(alpha = 0.20f), RoundedCornerShape(10.dp))
                .padding(10.dp),
            textStyle = androidx.compose.ui.text.TextStyle(
                color = themeColors.textPrimary.copy(alpha = 0.85f),
                fontSize = 10.sp,
                fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace
            ),
            cursorBrush = androidx.compose.ui.graphics.SolidColor(themeColors.accent),
            decorationBox = { inner ->
                if (importInput.isBlank()) {
                    Text(
                        "�ڴ�ճ�� MR.xxx.v1 ���Ե�������",
                        color = themeColors.textPrimary.copy(alpha = 0.35f),
                        fontSize = 10.sp,
                        fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace
                    )
                }
                inner()
            }
        )
        if (statusMsg.isNotBlank()) {
            Text(
                statusMsg,
                color = themeColors.accent,
                fontSize = 11.sp
            )
        }
    }
}
