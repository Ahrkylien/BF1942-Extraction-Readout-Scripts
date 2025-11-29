// DMeme: MEME decompiler version 1.6. Commercial use prohibited.
main()
{
	call BfLocale (0, BfLocaleData (Locale/Locale, $Locale/Valid$));

	Transform (0.000000, 0.000000, 800.000000, 600.000000)
	{
		if (!$ShowDebriefing$)
		{
			call Effect (BfMultiplyColor ($FocusEffect/BGAlpha$));
			call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
			call Picture ('');
		}
	}

	if ($TransitionEffect$)
	{
		if ($TransitionEffect$ == 1)
		{
			call TimeoutAction (ActionList (Set ($FocusEffect/BgPicAlpha$, 0.000000), Set ($FocusEffect/GoFadeOutLoadPicture$, true), Set ($FocusEffect/GoFadeOut2$, true), Set ($FocusEffect/GoMoveYOut$, true), 
					Set ($TransitionEffect$, 0)), 5.000000);
			call ActionNode (ActionList (Set ($FocusEffect/BGAlpha$, 0.000000)));
		}

		if ($TransitionEffect$ == 2)
		{
			call TimeoutAction (ActionList (Set ($FocusEffect/GoFadeIn$, true), Set ($FocusEffect/GoFadeInLoadPicture$, true), Set ($FocusEffect/GoMoveYIn$, true), Set ($FocusEffect/YPos$, 15.000000), Set ($TransitionEffect$, 
					0)), 1.000000);
			call ActionNode (ActionList (Set ($FocusEffect/Alpha$, 0.000000), Set ($FocusEffect/LoadAlpha$, 0.000000)));
		}

		if ($TransitionEffect$ == 3)
		{
			call TimeoutAction (ActionList (Set ($FocusEffect/GoFadeIn$, true), Set ($FocusEffect/GoMoveLeftIn$, true), Set ($FocusEffect/GoMoveRightIn$, true), Set ($FocusEffect/GoMoveYIn$, true), Set ($FocusEffect/LeftPos$, 
					-30.000000), Set ($FocusEffect/RightPos$, 30.000000), Set ($FocusEffect/YPos$, 30.000000), Set ($TransitionEffect$, 0)), 1.000000);
			call ActionNode (ActionList (Set ($FocusEffect/Alpha$, 0.000000), Set ($FocusEffect/BGAlpha$, 1.000000)));
		}

		if ($TransitionEffect$ == 4)
		{
			if (($StartingGame$ == 1) || ($StartingGame$ == 4))
			{
				call TimeoutAction (ActionList (Set ($FocusEffect/Abort$, 1), Set ($FocusEffect/GoFadeOut$, true), Set ($FocusEffect/GoMoveLeftOut$, true), Set ($FocusEffect/GoMoveRightOut$, true), Set ($FocusEffect/GoMoveYOut$, 
						true), Set ($TransitionEffect$, 0)), 1.000000);
			}

			if (($StartingGame$ == 0) || (($StartingGame$ == 3) || ($StartingGame$ == 2)))
			{
				call TimeoutAction (ActionList (Set ($FocusEffect/GoFadeOut$, true), Set ($FocusEffect/GoFadeOutLoadPicture$, true), Set ($FocusEffect/GoMoveYOut$, true), Set ($TransitionEffect$, 0)), 0.000000);
			}
		}

		if ($TransitionEffect$ == 5)
		{
			call TimeoutAction (ActionList (Set ($FocusEffect/GoFadeInButton$, true), Set ($TransitionEffect$, 0)), 3.000000);
			call ActionNode (ActionList (Set ($FocusEffect/ButtonAlpha$, 0.000000)));
		}

		if ($TransitionEffect$ == 6)
		{
			call TimeoutAction (ActionList (Set ($Load/ShowDefaultLoadingPicture$, false), Set ($FocusEffect/GoPictureSwitch$, true), Set ($TransitionEffect$, 0)), 0.000000);
			call ActionNode (ActionList (Set ($FocusEffect/LoadAlpha$, FloatRefData (0))));

			if ($FocusEffect/Alpha$ != 1.000000)
			{
				call TimeoutAction (ActionList (Set ($FocusEffect/GoFadeIn$, true), Set ($FocusEffect/GoMoveYIn$, true)), 0.000000);
				call ActionNode (ActionList (Set ($FocusEffect/Alpha$, 0.000000), Set ($FocusEffect/LoadAlpha$, 0.000000)));
			}
		}
	}

	if (!$ShowDebriefing$)
	{
		if ((($Load/LoadState$ == 0) || ($Load/LoadState$ == 5)) || (($Load/LoadState$ == 1) || ($Load/LoadState$ == 2)))
		{
			if (($StartingGame$ == 0) || (($StartingGame$ == 3) || ($StartingGame$ == 2)))
			{
				call BfAddSubNextEffect ($FocusEffect/Alpha$, 1, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (), $FocusEffect/GoFadeIn$);
				call BfAddSubNextEffect ($FocusEffect/LoadAlpha$, 1, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (), $FocusEffect/GoFadeInLoadPicture$);
				call BfAddSubNextEffect ($FocusEffect/YPos$, 1, 0.000000, 0.000000, 0.200000, 0.100000, false, ActionList (CallFunctionAction (Function (ContinueLoading))), $FocusEffect/GoMoveYIn$);
				call BfAddSubNextEffect ($FocusEffect/Alpha$, 0, 0.000000, 0.000000, 0.200000, 0.100000, false, ActionList (CallFunctionAction (Function (CancelLoading))), $FocusEffect/GoFadeOut$);
				call BfAddSubNextEffect ($FocusEffect/LoadAlpha$, 0, 0.000000, 0.000000, 0.200000, 0.100000, false, ActionList (), $FocusEffect/GoFadeOutLoadPicture$);
				call BfAddSubNextEffect ($FocusEffect/Alpha$, 0, 0.000000, 0.000000, 0.200000, 0.100000, false, ActionList (Set ($Load/LoadState$, 4), Set ($FocusEffect/GoFadeIn$, true), Set ($TransitionEffect$, 
						0)), $FocusEffect/GoFadeOut2$);
				call BfAddSubNextEffect ($FocusEffect/YPos$, 15, 0.000000, 0.000000, 0.200000, 0.000000, false, NULL, $FocusEffect/GoMoveYOut$);
				call BfAddSubNextEffect ($FocusEffect/LoadAlpha$, 1, 0.000000, 0.000000, 1.000000, 0.000000, false, ActionList (Set ($Load/ShowDefaultLoadingPicture$, false)), $FocusEffect/GoPictureSwitch$);

				Transform (0.000000, 0.000000, 800.000000, 600.000000)
				{
					Transform (0.000000, 85.000000, 800.000000, 450.000000)
					{
						call Effect (BfMultiplyColor ($FocusEffect/BgPicAlpha$));
						call Picture ('Menu/Background.tga');
					}

					call Effect (BfMultiplyColor ($FocusEffect/LoadAlpha$));

					if (!$Load/ShowDefaultLoadingPicture$)
					{
						call VariablePicture ($Load/LoadPicture$, NULL, NULL);
					}

					if ($Load/ShowDefaultLoadingPicture$)
					{
						Transform (0.000000, 85.000000, 800.000000, 450.000000)
						{
							call Picture ('Menu/Background.tga');
						}
					}
				}

				call Translate (0, $FocusEffect/YPos$);
				call Effect (BfMultiplyColor ($FocusEffect/Alpha$));

				Transform (260.000000, 465.000000, 512.000000, 64.000000)
				{
					call Picture ('Briefing/menu_loading.tga');

					Transform (10.000000, 6.000000, 268.000000, 16.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text ($Load/LevelName$, Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
					}

					Transform (17.000000, 33.000000, 258.000000, 18.000000)
					{
						Transform (0.000000, 0.000000, 260.000000, 18.000000)
						{
							call Effect (Color (0.546800, 0.546800, 0.546800, 1.000000));
							call Picture ('');
						}

						Transform (1.000000, 1.000000, 257.000000, 16.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Picture ('');
						}

						Transform (2.000000, 2.000000, 256.000000, 14.000000)
						{
							call BfVariablePictureFill ('loadingfull_256x16.tga', 'loading_full_256x16.tga', $Load/LoadPercent$, 100, 255, true, false);
						}
					}
				}

				Transform (0.000000, 535.000000, 800.000000, 20.000000)
				{
					call Effect (Color (0.843750, 0.730000, 0.650000, 1.000000));
					call Text ($Briefing/EscapeToCancel$, CenterAlignedStyle (0, 'standard6.dif'));
				}
			}

			if (($StartingGame$ == 1) || ($StartingGame$ == 4))
			{
				call BfAddSubEffect ($FocusEffect/Alpha$, 1, 0.000000, 0.000000, 0.200000, 0.000000, false, $FocusEffect/GoFadeIn$);
				call BfAddSubEffect ($FocusEffect/LeftPos$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, $FocusEffect/GoMoveLeftIn$);
				call BfAddSubEffect ($FocusEffect/RightPos$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, $FocusEffect/GoMoveRightIn$);
				call BfAddSubEffect ($FocusEffect/YPos$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, $FocusEffect/GoMoveYIn$);

				if ($FocusEffect/Abort$ == 0)
				{
					call BfAddSubNextEffect ($FocusEffect/Alpha$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, NULL, $FocusEffect/GoFadeOut$);
					call BfAddSubNextEffect ($FocusEffect/BGAlpha$, 0.000000, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (Set ($FocusEffect/BGAlpha$, 0.000000), CallFunctionAction (Function (StartSinglePlayer))), 
							$FocusEffect/GoFadeOut1$);
					call BfAddSubNextEffect ($FocusEffect/LeftPos$, -30, 0.000000, 0.000000, 0.200000, 0.000000, false, NULL, $FocusEffect/GoMoveLeftOut$);
					call BfAddSubNextEffect ($FocusEffect/RightPos$, 30, 0.000000, 0.000000, 0.200000, 0.000000, false, NULL, $FocusEffect/GoMoveRightOut$);
					call BfAddSubNextEffect ($FocusEffect/YPos$, 30, 0.000000, 0.000000, 0.200000, 0.000000, false, NULL, $FocusEffect/GoMoveYOut$);
				}

				if ($FocusEffect/Abort$ == 1)
				{
					call BfAddSubNextEffect ($FocusEffect/Alpha$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (CallFunctionAction (Function (CancelSinglePlayer))), $FocusEffect/GoFadeOut$);
					call BfAddSubNextEffect ($FocusEffect/LeftPos$, -30, 0.000000, 0.000000, 0.200000, 0.000000, false, NULL, $FocusEffect/GoMoveLeftOut$);
					call BfAddSubNextEffect ($FocusEffect/RightPos$, 30, 0.000000, 0.000000, 0.200000, 0.000000, false, NULL, $FocusEffect/GoMoveRightOut$);
				}

				Transform (0.000000, 85.000000, 800.000000, 450.000000)
				{
					call Effect (BfMultiplyColor ($FocusEffect/BGAlpha$));

					Transform (0.000000, -85.000000, 800.000000, 600.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Picture ('');
					}

					call Picture ('Menu/Background.tga');
				}

				call Effect (BfMultiplyColor ($FocusEffect/Alpha$));

				Transform (30.000000, 55.000000, 512.000000, 512.000000)
				{
					call Translate ($FocusEffect/LeftPos$, 0);
					call Picture ('Briefing/SP_briefing_512x512.tga');

					Transform (10.000000, 8.000000, 100.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_MAPNAME'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
					}

					Transform (4.000000, 27.000000, 512.000000, 512.000000)
					{
						call VariablePicture ($Briefing/BriefingPicture$, NULL, NULL);
					}
				}

				Transform (405.000000, 55.000000, 512.000000, 512.000000)
				{
					call Translate ($FocusEffect/RightPos$, 0);
					call Picture ('Briefing/SP_briefing_512x512.tga');

					Transform (10.000000, 8.000000, 100.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'BRIEFING_HEADING'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
					}

					Transform (10.000000, 32.000000, 340.000000, 350.000000)
					{
						call Text ($Briefing/BriefingText$, BfStyle (0, 'standard6.dif'));
					}
				}

				call Translate (0, $FocusEffect/YPos$);

				Transform (30.000000, 455.000000, 512.000000, 128.000000)
				{
					call Picture ('Briefing/SP_briefing_SMALL_512x128.tga');

					Transform (10.000000, 8.000000, 120.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'BRIEFING_OBJECTIVES_HEADING'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
					}

					Transform (10.000000, 35.000000, 320.000000, 65.000000)
					{
						call Text ($Briefing/ObjectivesText$, BfStyle (0, 'standard6.dif'));
					}
				}

				Transform (405.000000, 455.000000, 512.000000, 128.000000)
				{
					call Picture ('Briefing/SP_briefing_SMALL_512x128.tga');
					call BfAddSubNextEffect ($FocusEffect/ButtonAlpha$, 1, 0.000000, 0.000000, 0.500000, 0.000000, false, ActionList (Set ($Load/LoadState$, 2)), $FocusEffect/GoFadeInButton$);

					Transform (10.000000, 8.000000, 250.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text ($Load/LevelName$, Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
					}

					Transform (50.000000, 45.000000, 258.000000, 18.000000)
					{
						if ($Load/LoadState$ == 2)
						{
							call Effect (BfMultiplyColor (1.000000 - $FocusEffect/ButtonAlpha$));

							Transform (0.000000, 0.000000, 262.000000, 18.000000)
							{
								call Effect (Color (0.546800, 0.546800, 0.546800, 1.000000));
								call Picture ('');
							}

							Transform (2.000000, 1.000000, 258.000000, 16.000000)
							{
								call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
								call Picture ('');
							}

							Transform (3.000000, 2.000000, 256.000000, 14.000000)
							{
								call BfVariablePictureFill ('loadingfull_256x16.tga', 'loading_full_256x16.tga', $Load/LoadPercent$, 100, 256, true, false);
							}
						}
					}

					Transform (5.000000, 70.000000, 360.000000, 20.000000)
					{
						if ($Load/LoadState$ == 2)
						{
							call Effect (VariableColor (0.843750, 0.730000, 0.650000, 1.000000 - $FocusEffect/ButtonAlpha$));
							call Text ($Briefing/EscapeToCancel$, CenterAlignedStyle (0, 'standard6.dif'));
						}
					}

					Transform (50.000000, 45.000000, 258.000000, 18.000000)
					{
						if ($Load/LoadState$ == 1)
						{
							Transform (0.000000, 0.000000, 262.000000, 18.000000)
							{
								call Effect (Color (0.546800, 0.546800, 0.546800, 1.000000));
								call Picture ('');
							}

							Transform (2.000000, 1.000000, 258.000000, 16.000000)
							{
								call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
								call Picture ('');
							}

							Transform (3.000000, 2.000000, 256.000000, 14.000000)
							{
								call BfVariablePictureFill ('loadingfull_256x16.tga', 'loading_full_256x16.tga', $Load/LoadPercent$, 100, 256, true, false);
							}
						}
					}

					Transform (25.000000, 50.000000, 128.000000, 128.000000)
					{
						if (($Load/LoadState$ == 0) || ($Load/LoadState$ == 2))
						{
							call Effect (BfMultiplyColor ($FocusEffect/ButtonAlpha$));
							call BfButton ('Menu/knappExt_N.tga', 'Menu/knappExt_MO.tga', ActionList (Set ($FocusEffect/Abort$, 1), Set ($FocusEffect/GoFadeOut$, true), Set ($FocusEffect/GoFadeOut1$, true), Set ($FocusEffect/GoMoveLeftOut$, true), Set ($FocusEffect/GoMoveRightOut$, true)), 
									109.000000, 25.000000);

							Transform (5.000000, 9.000000, 96.000000, 18.000000)
							{
								call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'BRIEFING_ABORT'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
							}

							Transform (2.000000, 1.000000, 106.000000, 23.000000)
							{
								call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
								call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
							}
						}
					}

					Transform (225.000000, 50.000000, 128.000000, 128.000000)
					{
						if ($Load/LoadState$ == 0)
						{
							call BfButton ('Menu/knapp3_N.tga', 'Menu/knapp3_MO.tga', ActionList (CallFunctionAction (Function (LoadSinglePlayer))), 109.000000, 25.000000);

							Transform (8.000000, 9.000000, 97.000000, 18.000000)
							{
								call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'BRIEFING_LOAD'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
							}

							Transform (2.000000, 1.000000, 106.000000, 23.000000)
							{
								call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
								call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
							}
						}
					}

					Transform (225.000000, 50.000000, 128.000000, 128.000000)
					{
						if ($Load/LoadState$ == 2)
						{
							call Effect (BfMultiplyColor ($FocusEffect/ButtonAlpha$));
							call BfButton ('Menu/knapp3_N.tga', 'Menu/knapp3_MO.tga', ActionList (Set ($FocusEffect/Abort$, 0), Set ($FocusEffect/GoFadeOut$, true), Set ($FocusEffect/GoFadeOut1$, true), Set ($FocusEffect/GoMoveLeftOut$, true), Set ($FocusEffect/GoMoveRightOut$, true), 
									CallFunctionAction (Function (Sound/PlayLoadMenuStartGame))), 109.000000, 25.000000);

							Transform (8.000000, 9.000000, 97.000000, 18.000000)
							{
								call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'BRIEFING_PLAY'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
							}

							Transform (2.000000, 1.000000, 106.000000, 23.000000)
							{
								call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
								call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
							}
						}
					}

					if ($Load/LoadState$ == 1)
					{
						Transform (5.000000, 70.000000, 360.000000, 20.000000)
						{
							call Effect (Color (0.843750, 0.730000, 0.650000, 1.000000));
							call Text ($Briefing/EscapeToCancel$, CenterAlignedStyle (0, 'standard6.dif'));
						}
					}
				}
			}
		}

		if ($Load/LoadState$ == 4)
		{
			call BfAddSubNextEffect ($FocusEffect/Alpha$, 1, 0.000000, 0.000000, 0.300000, 1.000000, false, ActionList (Set ($FocusEffect/BGAlpha$, 0.000000)), $FocusEffect/GoFadeIn$);
			call BfAddSubEffect ($FocusEffect/BGAlpha$, 0, 0.000000, 0.000000, 0.300000, 1.000000, false, $FocusEffect/GoFadeIn$);
			call BfAddSubNextEffect ($FocusEffect/Alpha$, 0, 0.000000, 0.000000, 0.300000, 0.000000, false, ActionList (CallFunctionAction (Function (InfoMenu/DeActivateInfoMenu))), $FocusEffect/GoFadeOut$);

			Transform (0.000000, 0.000000, 800.000000, 600.000000)
			{
				call Effect (BfMultiplyColor ($FocusEffect/BGAlpha$));
				call Picture ('');
			}

			call Effect (BfMultiplyColor ($FocusEffect/Alpha$));

			Transform (144.000000, 80.000000, 512.000000, 512.000000)
			{
				call Picture ('Briefing/MP_briefing_512x512.tga');

				Transform (5.000000, -2.000000, 500.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text ($InfoMenu/InfoMenuHeading$, CenterAlignedStyle (Style/LoadHeadingStyle, 'Trebuchet MS18.dif'));
				}

				Transform (150.000000, 30.000000, 240.000000, 20.000000)
				{
					Transform (40.000000, 3.000000, 16.000000, 16.000000)
					{
						call VariablePicture ($AxisTicketFlagLoad$, NULL, NULL);
					}

					Transform (65.000000, 6.000000, 80.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_BRIEFING_VS'), CenterAlignedStyle (0, 'standard6.dif'));
					}

					Transform (150.000000, 3.000000, 16.000000, 16.000000)
					{
						call VariablePicture ($AlliedTicketFlagLoad$, NULL, NULL);
					}
				}

				Transform (4.000000, 58.000000, 504.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text ($InfoMenu/InfoMenuGameType$, CenterAlignedStyle (Style/LoadHeadingLatinCenter11, 'Trebuchet MS11 - Latin.dif'));
				}

				Transform (10.000000, 82.000000, 490.000000, 40.000000)
				{
					Transform (0.000000, 0.000000, 380.000000, 20.000000)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_BRIEFING_HEADING_1'), Style (0, 'standard6.dif'));
					}

					Transform (415.000000, 0.000000, 80.000000, 20.000000)
					{
						call Text ($InfoMenu/InfoMenuGeneralInfo1$, RightAlignedStyle (0, 'standard6.dif'));
					}

					Transform (0.000000, 15.000000, 380.000000, 20.000000)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_BRIEFING_HEADING_2'), Style (0, 'standard6.dif'));
					}

					Transform (415.000000, 15.000000, 80.000000, 20.000000)
					{
						call Text ($InfoMenu/InfoMenuGeneralInfo2$, RightAlignedStyle (0, 'standard6.dif'));
					}

					Transform (0.000000, 30.000000, 380.000000, 20.000000)
					{
						if (($Host/Create/GameType$ == 2) || ($Host/Create/GameType$ == 4))
						{
							if (!($StartingGame$ == 0))
							{
								call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_BRIEFING_HEADING_3'), Style (0, 'standard6.dif'));
							}
						}

						if (($Host/Create/GameType$ == 1) || ($Host/Create/GameType$ == 3))
						{
							if (!($StartingGame$ == 0))
							{
								call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_BRIEFING_HEADING_4'), Style (0, 'standard6.dif'));
							}
						}

						if ($StartingGame$ == 0)
						{
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'SINGLEPLAYER_NR_OF_LIVES'), Style (0, 'standard6.dif'));
						}
					}

					Transform (415.000000, 30.000000, 80.000000, 20.000000)
					{
						call Text ($InfoMenu/InfoMenuGeneralInfo3$, RightAlignedStyle (0, 'standard6.dif'));
					}
				}

				Transform (4.000000, 128.000000, 497.000000, 18.000000)
				{
					Transform (0.000000, 0.000000, 503.000000, 17.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Picture ('');
					}

					Transform (1.000000, 1.000000, 501.000000, 15.000000)
					{
						call Effect (Color (0.519531, 0.492190, 0.300781, 1.000000));
						call Picture ('');
					}

					Transform (6.000000, 4.000000, 100.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_BRIEFING_OBJECTIVES'), Style (0, 'standard6.dif'));
					}
				}

				Transform (10.000000, 145.000000, 490.000000, 78.000000)
				{
					call Text ($InfoMenu/InfoMenuObjectives$, BfStyle (0, 'standard6.dif'));
				}

				Transform (4.000000, 230.000000, 497.000000, 18.000000)
				{
					Transform (0.000000, 0.000000, 503.000000, 17.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Picture ('');
					}

					Transform (1.000000, 1.000000, 501.000000, 15.000000)
					{
						call Effect (Color (0.519531, 0.492190, 0.300781, 1.000000));
						call Picture ('');
					}

					Transform (6.000000, 4.000000, 100.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_BRIEFING_COMMENTS'), Style (0, 'standard6.dif'));
					}
				}

				Transform (10.000000, 250.000000, 490.000000, 75.000000)
				{
					Transform (0.000000, 0.000000, 490.000000, 20.000000)
					{
						call Text ($InfoMenu/InfoMenuComments1$, Style (0, 'standard6.dif'));
					}

					Transform (0.000000, 15.000000, 490.000000, 20.000000)
					{
						call Text ($InfoMenu/InfoMenuComments2$, Style (0, 'standard6.dif'));
					}

					Transform (0.000000, 30.000000, 490.000000, 20.000000)
					{
						call Text ($InfoMenu/InfoMenuComments3$, Style (0, 'standard6.dif'));
					}

					Transform (0.000000, 45.000000, 490.000000, 20.000000)
					{
						call Text ($InfoMenu/InfoMenuComments4$, Style (0, 'standard6.dif'));
					}

					Transform (0.000000, 60.000000, 490.000000, 20.000000)
					{
						call Text ($InfoMenu/InfoMenuComments5$, Style (0, 'standard6.dif'));
					}
				}
			}

			Transform (144.000000, 417.000000, 512.000000, 64.000000)
			{
				call Picture ('Ingame/respawn/ingame_respawn_long_512x64.tga');

				Transform (192.000000, 8.000000, 128.000000, 128.000000)
				{
					call BfButton ('Menu/knapp3_N.tga', 'Menu/knapp3_MO.tga', ActionList (Set ($FocusEffect/GoFadeOut$, true), CallFunctionAction (Function (Sound/PlayLoadMenuStartGame))), 109.000000, 25.000000);

					Transform (8.000000, 9.000000, 97.000000, 18.000000)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MULTIPLAYER_BRIEFING_READY'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
					}

					Transform (2.000000, 1.000000, 106.000000, 23.000000)
					{
						call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
						call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
					}
				}
			}
		}

		call CullVariableAndEventAction (ActionList (CallFunctionAction (Function (InfoMenu/DeActivateInfoMenu)), CallFunctionAction (Function (Sound/PlayLoadMenuStartGame))), $Load/LoadState$ == 4, ExtendedButtonEvent (0, 
				1, 18, 1));
		call ActionNode (Set ($FocusEffect/DebriefingAlpha$, 1.000000));
	}

	if (($ShowDebriefing$ == 1) || ($ShowDebriefing$ == 2))
	{
		Transform (150.000000, 100.000000, 512.000000, 512.000000)
		{
			if (($StartingGame$ == 2) || ($StartingGame$ == 3))
			{
				call Picture ('Debriefing/MP_debriefing_512x512.tga');

				Transform (5.000000, -2.000000, 500.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text ($Debriefing/DebriefingHeading$, CenterAlignedStyle (Style/LoadHeadingStyle, 'Trebuchet MS18.dif'));
				}

				Transform (150.000000, 30.000000, 240.000000, 20.000000)
				{
					Transform (22.000000, 3.000000, 16.000000, 16.000000)
					{
						call VariablePicture ($AxisTicketFlagLoad$, NULL, NULL);
					}

					Transform (42.000000, 1.000000, 40.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text ($AxisTicket$, Style (Style/LoadHeadingLatin11, 'Trebuchet MS11 - Latin.dif'));
					}
				}

				Transform (250.000000, 30.000000, 240.000000, 20.000000)
				{
					Transform (22.000000, 3.000000, 16.000000, 16.000000)
					{
						call VariablePicture ($AlliedTicketFlagLoad$, NULL, NULL);
					}

					Transform (42.000000, 1.000000, 40.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text ($AlliedTicket$, Style (Style/LoadHeadingLatin11, 'Trebuchet MS11 - Latin.dif'));
					}
				}

				Transform (8.000000, 61.000000, 185.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_HEADING'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
				}

				Transform (4.000000, 78.000000, 512.000000, 32.000000)
				{
					Transform (0.000000, 0.000000, 502.000000, 18.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Picture ('');
					}

					Transform (1.000000, 1.000000, 501.000000, 16.000000)
					{
						call Effect (Color (0.519531, 0.492190, 0.300781, 1.000000));
						call Picture ('');
					}

					Transform (50.000000, 4.000000, 100.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_PLAYER_NAME'), Style (0, 'standard6.dif'));
					}

					Transform (218.000000, 1.000000, 16.000000, 16.000000)
					{
						call Picture ('Menu/serverinfo/menu_icon_score_16x16.tga');
					}

					Transform (266.000000, 1.000000, 16.000000, 16.000000)
					{
						call Picture ('Menu/serverinfo/menu_icon_kills_16x16.tga');
					}

					Transform (318.000000, 1.000000, 16.000000, 16.000000)
					{
						call Picture ('Menu/serverinfo/menu_icon_death_16x16.tga');
					}

					Transform (370.000000, 2.000000, 16.000000, 16.000000)
					{
						call Picture ('Menu/serverinfo/menu_icon_ping_16x16.tga');
					}
				}

				Transform (-5.000000, -45.000000, 500.000000, 500.000000)
				{
					call BfNewListBox (BfListBoxData (Debriefing/DebriefingList, NULL, NULL, NULL), 'standard6.dif', NULL, NULL, false, false, false, 76.000000, false, true, 0.000000, 0.000000, 0.000000, 0.000000, 4.000000, 1.000000, 1.000000, 1.000000, 0.000000, 0.000000, 0.187500, 0.539000, 0.800000, false, 4.000000);
				}
			}
		}

		Transform (162.000000, 20.000000, 512.000000, 512.000000)
		{
			if (($StartingGame$ == 0) || (($StartingGame$ == 1) || ($StartingGame$ == 4)))
			{
				call Effect (BfMultiplyColor ($FocusEffect/DebriefingAlpha$));
				call Picture ('Debriefing/SP_debriefing_512x512.tga');

				Transform (5.000000, -2.000000, 500.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text ($Debriefing/DebriefingHeading$, CenterAlignedStyle (Style/LoadHeadingStyle, 'Trebuchet MS18.dif'));
				}

				Transform (150.000000, 30.000000, 240.000000, 20.000000)
				{
					Transform (22.000000, 3.000000, 16.000000, 16.000000)
					{
						call VariablePicture ($AxisTicketFlagLoad$, NULL, NULL);
					}

					Transform (42.000000, 1.000000, 20.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text ($AxisTicket$, Style (Style/LoadHeadingLatin11, 'Trebuchet MS11 - Latin.dif'));
					}
				}

				Transform (250.000000, 30.000000, 240.000000, 20.000000)
				{
					Transform (22.000000, 3.000000, 16.000000, 16.000000)
					{
						call VariablePicture ($AlliedTicketFlagLoad$, NULL, NULL);
					}

					Transform (42.000000, 1.000000, 20.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text ($AlliedTicket$, Style (Style/LoadHeadingLatin11, 'Trebuchet MS11 - Latin.dif'));
					}
				}

				Transform (8.000000, 56.000000, 490.000000, 114.000000)
				{
					call Text ($Debriefing/DebriefingText$, BfStyle (0, 'standard6.dif'));
				}

				Transform (10.000000, 180.000000, 500.000000, 20.000000)
				{
					if (($StartingGame$ == 1) || ($StartingGame$ == 4))
					{
						Transform (6.000000, 2.000000, 201.000000, 23.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_CAMPAIGN_STATUS'), RightAlignedStyle (0, 'standard6.dif'));
						}

						Transform (220.000000, -2.000000, 128.000000, 16.000000)
						{
							call BfVariablePictureFill ('Debriefing/statusbar.tga', 'Debriefing/statusbar_full.tga', $CampaignScore$, $MaxCampaignScore$, 93, true, true);
						}
					}
				}

				Transform (5.000000, 198.000000, 497.000000, 18.000000)
				{
					Transform (0.000000, 0.000000, 502.000000, 18.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Picture ('');
					}

					Transform (1.000000, 1.000000, 501.000000, 16.000000)
					{
						call Effect (Color (0.519531, 0.492190, 0.300781, 1.000000));
						call Picture ('');
					}

					Transform (22.000000, 4.000000, 100.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_PLAYER_NAME'), Style (0, 'standard6.dif'));
					}

					Transform (218.000000, 1.000000, 16.000000, 16.000000)
					{
						call Picture ('Menu/serverinfo/menu_icon_score_16x16.tga');
					}

					Transform (266.000000, 1.000000, 16.000000, 16.000000)
					{
						call Picture ('Menu/serverinfo/menu_icon_kills_16x16.tga');
					}

					Transform (318.000000, 1.000000, 16.000000, 16.000000)
					{
						call Picture ('Menu/serverinfo/menu_icon_death_16x16.tga');
					}

					if (false)
					{
						Transform (220.000000, 4.000000, 100.000000, 20.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_SCORE'), Style (0, 'standard6.dif'));
						}

						Transform (270.000000, 4.000000, 100.000000, 20.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_KILLS'), Style (0, 'standard6.dif'));
						}

						Transform (320.000000, 4.000000, 100.000000, 20.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_DEATHS'), Style (0, 'standard6.dif'));
						}

						Transform (370.000000, 4.000000, 100.000000, 20.000000)
						{
							if (false)
							{
								call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
								call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_PING'), Style (0, 'standard6.dif'));
							}
						}
					}
				}

				Transform (-5.000000, 198.000000, 500.000000, 500.000000)
				{
					call BfNewListBox (BfListBoxData (Debriefing/DebriefingList, NULL, NULL, NULL), 'standard6.dif', NULL, NULL, false, false, false, 14.000000, false, true, 0.000000, 0.000000, 0.000000, 0.000000, 4.000000, 1.000000, 1.000000, 1.000000, 0.000000, 0.000000, 0.187500, 0.539000, 0.800000, false, 4.000000);
				}

				Transform (5.000000, 292.000000, 512.000000, 32.000000)
				{
					Transform (0.000000, 0.000000, 502.000000, 17.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Picture ('');
					}

					Transform (1.000000, 1.000000, 501.000000, 15.000000)
					{
						call Effect (Color (0.519531, 0.492190, 0.300781, 1.000000));
						call Picture ('');
					}

					Transform (5.000000, 4.000000, 200.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_STATISTICS'), Style (0, 'standard6.dif'));
					}
				}

				Transform (5.000000, 291.000000, 492.000000, 230.000000)
				{
					call BfNewListBox (BfListBoxData (Debriefing/DebriefingStatisticsList, NULL, NULL, NULL), 'standard6.dif', NULL, NULL, false, false, false, 15.000000, false, false, 0.000000, 0.000000, 0.000000, 0.000000, 6.000000, 1.000000, 1.000000, 1.000000, 0.000000, 0.492190, 0.535160, 0.289100, 1.000000, false, 4.000000);
				}
			}
		}

		Transform (162.000000, 535.000000, 512.000000, 64.000000)
		{
			if (($StartingGame$ == 0) || (($StartingGame$ == 1) || ($StartingGame$ == 4)))
			{
				call Effect (BfMultiplyColor ($FocusEffect/DebriefingAlpha$));
				call Picture ('Debriefing/SP_debriefing_SMALL_512x64.tga');

				if (($StartingGame$ == 1) || ($StartingGame$ == 4))
				{
					Transform (10.000000, 7.000000, 128.000000, 128.000000)
					{
						call BfButton ('Menu/knapp3_N.tga', 'Menu/knapp3_MO.tga', ActionList (Set ($FocusEffect/GoFadeOut1$, true)), 109.000000, 25.000000);
						call BfAddSubNextEffect ($FocusEffect/DebriefingAlpha$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (CallFunctionAction (Function (DoneCampaign))), $FocusEffect/GoFadeOut1$);

						Transform (5.000000, 9.000000, 96.000000, 18.000000)
						{
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_DONE'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
						}

						Transform (2.000000, 1.000000, 106.000000, 23.000000)
						{
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
						}
					}

					Transform (200.000000, 7.000000, 128.000000, 128.000000)
					{
						call BfButton ('Menu/knapp3_N.tga', 'Menu/knapp3_MO.tga', ActionList (Set ($FocusEffect/GoFadeOut2$, true)), 109.000000, 25.000000);
						call BfAddSubNextEffect ($FocusEffect/DebriefingAlpha$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (CallFunctionAction (Function (ReplayCampaign))), $FocusEffect/GoFadeOut2$);

						Transform (5.000000, 9.000000, 96.000000, 18.000000)
						{
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_REPLAY'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
						}

						Transform (2.000000, 1.000000, 106.000000, 23.000000)
						{
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
						}
					}

					Transform (390.000000, 7.000000, 128.000000, 128.000000)
					{
						call BfButton ('Menu/knapp3_N.tga', 'Menu/knapp3_MO.tga', ActionList (Set ($FocusEffect/GoFadeOut3$, true)), 109.000000, 25.000000);
						call BfAddSubNextEffect ($FocusEffect/DebriefingAlpha$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (CallFunctionAction (Function (NextCampaign))), $FocusEffect/GoFadeOut3$);

						Transform (5.000000, 9.000000, 96.000000, 18.000000)
						{
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_CONTINUE'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
						}

						Transform (2.000000, 1.000000, 106.000000, 23.000000)
						{
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
						}
					}
				}

				if ($StartingGame$ == 0)
				{
					Transform (10.000000, 7.000000, 128.000000, 128.000000)
					{
						call BfButton ('Menu/knappExt_N.tga', 'Menu/knappExt_MO.tga', ActionList (Set ($FocusEffect/GoFadeOut1$, true)), 109.000000, 25.000000);
						call BfAddSubNextEffect ($FocusEffect/DebriefingAlpha$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (CallFunctionAction (Function (DoneSkirmish))), $FocusEffect/GoFadeOut1$);

						Transform (5.000000, 9.000000, 96.000000, 18.000000)
						{
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_ABORT'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
						}

						Transform (2.000000, 1.000000, 106.000000, 23.000000)
						{
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
						}
					}

					Transform (390.000000, 7.000000, 128.000000, 128.000000)
					{
						call BfButton ('Menu/knapp3_N.tga', 'Menu/knapp3_MO.tga', ActionList (Set ($FocusEffect/GoFadeOut2$, true)), 109.000000, 25.000000);
						call BfAddSubNextEffect ($FocusEffect/DebriefingAlpha$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (CallFunctionAction (Function (ReplaySkirmish))), $FocusEffect/GoFadeOut2$);

						Transform (5.000000, 9.000000, 96.000000, 18.000000)
						{
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_REPLAY'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
						}

						Transform (2.000000, 1.000000, 106.000000, 23.000000)
						{
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
						}
					}

					if (false)
					{
						if ($InhibitMenuBehavior$ == 3)
						{
							Transform (200.000000, 7.000000, 128.000000, 128.000000)
							{
								call BfButton ('Menu/knappExt_N.tga', 'Menu/knappExt_MO.tga', ActionList (CallFunctionAction (Function (DoneSkirmish))), 107.000000, 24.000000);

								Transform (5.000000, 9.000000, 96.000000, 18.000000)
								{
									call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_ABORT'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
								}

								Transform (3.000000, 0.000000, 107.000000, 24.000000)
								{
									call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
									call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
								}
							}
						}
					}
				}
			}
		}
	}

	Transform (0.000000, 0.000000, 800.000000, 600.000000)
	{
		if ($ShowDebriefing$ == 3)
		{
			call Effect (BfMultiplyColor ($FocusEffect/SplashScreenAlpha$));

			if (($CampaignVictory$ == 1) || (($CampaignVictory$ == 2) || ($CampaignVictory$ == 3)))
			{
				call CullEventAction (ActionList (Set ($Debriefing/ShowHeading$, false), Set ($Debriefing/ShowCampaignDebriefing$, true), SetStringAction ($Debriefing/DebriefingText$, BfLocaleString (BfLocaleData (Locale/Locale, 
						$Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_ALLIED_VICTORY_HISTORIC'))), ButtonEvent (0, 1, 1));
				call Picture ('Debriefing/Allied_Win_Camp.tga');

				Transform (0.000000, 200.000000, 800.000000, 20.000000)
				{
					if ($Debriefing/ShowHeading$)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_ALLIED_VICTORY'), CenterAlignedStyle (0, 'Trebuchet MS8.dif'));
					}
				}
			}

			if (($CampaignVictory$ == 4) || (($CampaignVictory$ == 5) || ($CampaignVictory$ == 6)))
			{
				call CullEventAction (ActionList (Set ($Debriefing/ShowHeading$, false), Set ($Debriefing/ShowCampaignDebriefing$, true), SetStringAction ($Debriefing/DebriefingText$, BfLocaleString (BfLocaleData (Locale/Locale, 
						$Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_AXIS_VICTORY_HISTORIC'))), ButtonEvent (0, 1, 1));
				call Picture ('Debriefing/Axis_Win_Camp.tga');

				Transform (0.000000, 200.000000, 800.000000, 20.000000)
				{
					if ($Debriefing/ShowHeading$)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_AXIS_VICTORY'), CenterAlignedStyle (0, 'Trebuchet MS8.dif'));
					}
				}
			}

			if (($CampaignVictory$ == 7) || (($CampaignVictory$ == 8) || ($CampaignVictory$ == 9)))
			{
				call CullEventAction (ActionList (Set ($Debriefing/ShowHeading$, false), Set ($Debriefing/ShowCampaignDebriefing$, true), SetStringAction ($Debriefing/DebriefingText$, BfLocaleString (BfLocaleData (Locale/Locale, 
						$Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_ALLIED_DEFEAT_HISTORIC'))), ButtonEvent (0, 1, 1));
				call Picture ('Debriefing/Allied_Lose_Camp.tga');

				Transform (0.000000, 200.000000, 800.000000, 20.000000)
				{
					if ($Debriefing/ShowHeading$)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_ALLIED_DEFEAT'), CenterAlignedStyle (0, 'Trebuchet MS8.dif'));
					}
				}
			}

			if (($CampaignVictory$ == 10) || (($CampaignVictory$ == 11) || ($CampaignVictory$ == 12)))
			{
				call CullEventAction (ActionList (Set ($Debriefing/ShowHeading$, false), Set ($Debriefing/ShowCampaignDebriefing$, true), SetStringAction ($Debriefing/DebriefingText$, BfLocaleString (BfLocaleData (Locale/Locale, 
						$Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_AXIS_DEFEAT_HISTORIC'))), ButtonEvent (0, 1, 1));
				call Picture ('Debriefing/Axis_Lose_Camp.tga');

				Transform (0.000000, 200.000000, 800.000000, 20.000000)
				{
					if ($Debriefing/ShowHeading$)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_AXIS_DEFEAT'), CenterAlignedStyle (0, 'Trebuchet MS8.dif'));
					}
				}
			}

			Transform (162.000000, 20.000000, 512.000000, 512.000000)
			{
				if ($Debriefing/ShowCampaignDebriefing$)
				{
					call Picture ('Debriefing/SP_debriefing_512x512.tga');

					Transform (5.000000, -3.000000, 500.000000, 20.000000)
					{
						call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
						call Text ($Debriefing/DebriefingHeading$, CenterAlignedStyle (0, 'Trebuchet MS18.dif'));
					}

					Transform (8.000000, 56.000000, 490.000000, 114.000000)
					{
						call Text ($Debriefing/DebriefingText$, BfStyle (0, 'standard6.dif'));
					}

					Transform (10.000000, 180.000000, 500.000000, 20.000000)
					{
						Transform (6.000000, 2.000000, 201.000000, 23.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_CAMPAIGN_STATUS_FINAL'), RightAlignedStyle (0, 'standard6.dif'));
						}

						Transform (220.000000, -3.000000, 128.000000, 16.000000)
						{
							call BfVariablePictureFill ('Debriefing/statusbar.tga', 'Debriefing/statusbar_full.tga', $CampaignScore$, $MaxCampaignScore$, 93, true, true);
						}
					}

					Transform (4.000000, 198.000000, 497.000000, 18.000000)
					{
						Transform (0.000000, 0.000000, 503.000000, 17.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Picture ('');
						}

						Transform (1.000000, 1.000000, 501.000000, 15.000000)
						{
							call Effect (Color (0.519531, 0.492190, 0.300781, 1.000000));
							call Picture ('');
						}

						Transform (22.000000, 4.000000, 100.000000, 20.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_PLAYER_NAME'), Style (0, 'standard6.dif'));
						}

						Transform (220.000000, 4.000000, 100.000000, 20.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_SCORE'), Style (0, 'standard6.dif'));
						}

						Transform (270.000000, 4.000000, 100.000000, 20.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_KILLS'), Style (0, 'standard6.dif'));
						}

						Transform (320.000000, 4.000000, 100.000000, 20.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'COL_HEADING_DEATHS'), Style (0, 'standard6.dif'));
						}
					}

					Transform (-5.000000, 198.000000, 500.000000, 50.000000)
					{
						call BfNewListBox (BfListBoxData (Debriefing/DebriefingList, NULL, NULL, NULL), 'standard6.dif', NULL, NULL, false, false, false, 14.000000, false, true, 0.000000, 0.000000, 0.000000, 0.000000, 4.000000, 1.000000, 1.000000, 1.000000, 0.000000, 0.000000, 0.187500, 0.539000, 0.800000, false, 4.000000);
					}

					Transform (5.000000, 293.000000, 512.000000, 32.000000)
					{
						Transform (0.000000, 0.000000, 502.000000, 17.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Picture ('');
						}

						Transform (1.000000, 1.000000, 501.000000, 15.000000)
						{
							call Effect (Color (0.519531, 0.492190, 0.300781, 1.000000));
							call Picture ('');
						}

						Transform (5.000000, 4.000000, 200.000000, 20.000000)
						{
							call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_STATISTICS'), Style (0, 'standard6.dif'));
						}
					}

					Transform (5.000000, 291.000000, 492.000000, 230.000000)
					{
						call BfNewListBox (BfListBoxData (Debriefing/DebriefingStatisticsList, NULL, NULL, NULL), 'standard6.dif', NULL, NULL, false, false, false, 14.000000, false, false, 0.000000, 0.000000, 0.000000, 0.000000, 6.000000, 1.000000, 1.000000, 1.000000, 0.000000, 0.492190, 0.535160, 0.289100, 1.000000, false, 4.000000);
					}
				}
			}

			Transform (0.000000, 0.000000, 20.000000, 20.000000)
			{
				if (false)
				{
					call Picture ('');
					call CullEventAction (ActionList (Set ($Debriefing/ShowCampaignDebriefing$, false), Set ($Debriefing/ShowHeading$, true)), ButtonEvent (0, 1, 1));
				}
			}

			Transform (162.000000, 535.000000, 512.000000, 64.000000)
			{
				if (($StartingGame$ == 0) || (($StartingGame$ == 1) || ($StartingGame$ == 4)))
				{
					call Picture ('Debriefing/SP_debriefing_SMALL_512x64.tga');

					Transform (200.000000, 7.000000, 128.000000, 128.000000)
					{
						call BfButton ('Menu/knapp3_N.tga', 'Menu/knapp3_MO.tga', ActionList (Set ($FocusEffect/GoFadeOut1$, true)), 109.000000, 25.000000);
						call BfAddSubNextEffect ($FocusEffect/SplashScreenAlpha$, 0, 0.000000, 0.000000, 0.200000, 0.000000, false, ActionList (CallFunctionAction (Function (DoneCampaign))), $FocusEffect/GoFadeOut1$);

						Transform (5.000000, 9.000000, 96.000000, 18.000000)
						{
							call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'DEBRIEFING_DONE'), CenterAlignedStyle (Style/LoadNavigationStyle, 'standard6.dif'));
						}

						Transform (2.000000, 1.000000, 106.000000, 23.000000)
						{
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuCancel)), ButtonEvent (0, 1, 1));
							call CullEventAction (CallFunctionAction (Function (Sound/PlayLoadMenuHighLight)), TypeEvent (0, 9));
						}
					}
				}
			}
		}
	}

	Transform (261.000000, 258.000000, 512.000000, 128.000000)
	{
		if ($Password/ShowPassword$)
		{
			Transform (0.000000, 25.000000, 273.000000, 80.000000)
			{
				call Effect (Color (0.000000, 0.000000, 0.000000, 0.800000));
				call Picture ('');
			}

			call Picture ('Menu/menu_addserver_512x128.tga');

			Transform (10.000000, 8.000000, 268.000000, 16.000000)
			{
				call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
				call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MENU_PASSWORD'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
			}

			Transform (5.000000, 35.000000, 267.000000, 20.000000)
			{
				if ($Password/ShowPassword$ == 1)
				{
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'PASSWORD_INVALID'), CenterAlignedStyle (0, 'standard6.dif'));
				}

				if ($Password/ShowPassword$ == 2)
				{
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'PASSWORD_INVALID_FIRST_ATTEMPT'), CenterAlignedStyle (0, 'standard6.dif'));
				}
			}

			Transform (40.000000, 50.000000, 200.000000, 20.000000)
			{
				Transform (13.000000, 0.000000, 174.000000, 19.000000)
				{
					call Effect (Color (0.546800, 0.546800, 0.546800, 1.000000));
					call Picture ('');
				}

				Transform (14.000000, 1.000000, 172.000000, 17.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Picture ('');
				}

				Transform (17.000000, 5.000000, 165.000000, 20.000000)
				{
					call Effect (Color (1.000000, 1.000000, 1.000000, 1.000000));
					call BfEdit ('standard6.dif', $Password/NewPassword$, 30, NULL, NULL, false);
				}
			}

			Transform (15.000000, 80.000000, 64.000000, 32.000000)
			{
				call BfButton ('Menu/buttons/menu_reset_64x32.tga', 'Menu/buttons/menu_reset_MO_64x32.tga', ActionList (Set ($Password/ShowPassword$, 0), CallFunctionAction (Function (Password/CancelPassword))), 63.000000, 20.000000);

				Transform (2.000000, 5.000000, 63.000000, 20.000000)
				{
					call Effect (Color (1.000000, 1.000000, 1.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MENU_CANCEL'), CenterAlignedStyle (0, 'standard6.dif'));
				}

				Transform (1.000000, 1.000000, 61.000000, 18.000000)
				{
					call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuOk)), TypeEvent (0, 1));
					call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuHighLight)), TypeEvent (0, 9));
				}
			}

			Transform (200.000000, 80.000000, 64.000000, 32.000000)
			{
				call BfButton ('Menu/buttons/menu_reset_64x32.tga', 'Menu/buttons/menu_reset_MO_64x32.tga', ActionList (Set ($Password/ShowPassword$, 0), CallFunctionAction (Function (Password/JoinPassword))), 63.000000, 20.000000);

				Transform (2.000000, 5.000000, 63.000000, 20.000000)
				{
					call Effect (Color (1.000000, 1.000000, 1.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'MENU_OK'), CenterAlignedStyle (0, 'standard6.dif'));
				}

				Transform (1.000000, 1.000000, 61.000000, 18.000000)
				{
					call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuOk)), TypeEvent (0, 1));
					call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuHighLight)), TypeEvent (0, 9));
				}
			}
		}
	}

	if ($Join/ShowFailedToJoin$)
	{
		Transform (0.000000, 0.000000, 800.000000, 600.000000)
		{
			call Effect (Color (0.000000, 0.000000, 0.000000, 0.400000));
			call Picture ('');
		}

		Transform (265.000000, 200.000000, 512.000000, 128.000000)
		{
			call Picture ('Menu/menu_addserver_512x128.tga');
		}

		if ($Join/ShowFailedToJoin$ == 1)
		{
			Transform (265.000000, 200.000000, 512.000000, 128.000000)
			{
				Transform (10.000000, 8.000000, 120.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_ERROR'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
				}

				Transform (10.000000, 50.000000, 260.000000, 20.000000)
				{
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_FAILED_TO_CONNECT'), CenterAlignedStyle (0, 'standard6.dif'));
				}

				Transform (110.000000, 80.000000, 64.000000, 32.000000)
				{
					call BfButton ('Menu/buttons/menu_reset_64x32.tga', 'Menu/buttons/menu_reset_MO_64x32.tga', ActionList (CallFunctionAction (Function (Join/FailedToJoin))), 63.000000, 20.000000);

					Transform (0.000000, 5.000000, 63.000000, 20.000000)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_OK'), CenterAlignedStyle (0, 'standard6.dif'));
					}

					Transform (1.000000, 1.000000, 61.000000, 18.000000)
					{
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuOk)), TypeEvent (0, 1));
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuHighLight)), TypeEvent (0, 9));
					}
				}
			}
		}

		if ($Join/ShowFailedToJoin$ == 2)
		{
			Transform (265.000000, 200.000000, 512.000000, 128.000000)
			{
				Transform (10.000000, 8.000000, 120.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_ERROR'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
				}

				Transform (10.000000, 50.000000, 260.000000, 20.000000)
				{
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_FAILED_TO_CONNECT_OLD_VERSION'), BfCenterStyle (0, 'standard6.dif'));
				}

				Transform (15.000000, 80.000000, 64.000000, 32.000000)
				{
					call BfButton ('Menu/buttons/menu_reset_64x32.tga', 'Menu/buttons/menu_reset_MO_64x32.tga', ActionList (Set ($Join/ShowFailedToJoin$, 3), CallFunctionAction (Function (Join/UpdateVersion))), 63.000000, 20.000000);

					Transform (0.000000, 5.000000, 63.000000, 20.000000)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_YES'), CenterAlignedStyle (0, 'standard6.dif'));
					}

					Transform (1.000000, 1.000000, 61.000000, 18.000000)
					{
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuOk)), TypeEvent (0, 1));
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuHighLight)), TypeEvent (0, 9));
					}
				}

				Transform (200.000000, 80.000000, 64.000000, 32.000000)
				{
					call BfButton ('Menu/buttons/menu_reset_64x32.tga', 'Menu/buttons/menu_reset_MO_64x32.tga', ActionList (CallFunctionAction (Function (Join/FailedToJoin))), 63.000000, 20.000000);

					Transform (0.000000, 5.000000, 63.000000, 20.000000)
					{
						call Effect (Color (1.000000, 1.000000, 1.000000, 1.000000));
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_NO'), CenterAlignedStyle (0, 'standard6.dif'));
					}

					Transform (1.000000, 1.000000, 61.000000, 18.000000)
					{
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuOk)), TypeEvent (0, 1));
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuHighLight)), TypeEvent (0, 9));
					}
				}
			}
		}

		if ($Join/ShowFailedToJoin$ == 3)
		{
			Transform (265.000000, 200.000000, 512.000000, 128.000000)
			{
				Transform (10.000000, 8.000000, 120.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_HEADING_INFO'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
				}

				Transform (10.000000, 50.000000, 260.000000, 20.000000)
				{
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_LOOKING_FOR_UPDATES'), BfCenterStyle (0, 'standard6.dif'));
				}

				Transform (110.000000, 80.000000, 64.000000, 32.000000)
				{
					call BfButton ('Menu/buttons/menu_reset_64x32.tga', 'Menu/buttons/menu_reset_MO_64x32.tga', ActionList (CallFunctionAction (Function (Join/FailedToJoin))), 63.000000, 20.000000);

					Transform (0.000000, 5.000000, 63.000000, 20.000000)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_ABORT'), CenterAlignedStyle (0, 'standard6.dif'));
					}

					Transform (1.000000, 1.000000, 61.000000, 18.000000)
					{
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuOk)), TypeEvent (0, 1));
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuHighLight)), TypeEvent (0, 9));
					}
				}
			}
		}

		if ($Join/ShowFailedToJoin$ == 4)
		{
			Transform (265.000000, 200.000000, 512.000000, 128.000000)
			{
				Transform (10.000000, 8.000000, 120.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_WARNING'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
				}

				Transform (10.000000, 50.000000, 260.000000, 20.000000)
				{
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_FAILED_TO_CONNECT_SERVER_FULL'), CenterAlignedStyle (0, 'standard6.dif'));
				}

				Transform (110.000000, 80.000000, 64.000000, 32.000000)
				{
					call BfButton ('Menu/buttons/menu_reset_64x32.tga', 'Menu/buttons/menu_reset_MO_64x32.tga', ActionList (CallFunctionAction (Function (Join/FailedToJoin))), 63.000000, 20.000000);

					Transform (0.000000, 5.000000, 63.000000, 20.000000)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_OK'), CenterAlignedStyle (0, 'standard6.dif'));
					}

					Transform (1.000000, 1.000000, 61.000000, 18.000000)
					{
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuOk)), TypeEvent (0, 1));
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuHighLight)), TypeEvent (0, 9));
					}
				}
			}
		}

		if ($Join/ShowFailedToJoin$ == 5)
		{
			Transform (265.000000, 200.000000, 512.000000, 128.000000)
			{
				Transform (10.000000, 8.000000, 120.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_ERROR'), Style (Style/LoadHeading8, 'Trebuchet MS8.dif'));
				}

				Transform (10.000000, 50.000000, 260.000000, 20.000000)
				{
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'ERROR_BANNED_FROM_SERVER'), CenterAlignedStyle (0, 'standard6.dif'));
				}

				Transform (110.000000, 80.000000, 64.000000, 32.000000)
				{
					call BfButton ('Menu/buttons/menu_reset_64x32.tga', 'Menu/buttons/menu_reset_MO_64x32.tga', ActionList (CallFunctionAction (Function (Join/FailedToJoin))), 63.000000, 20.000000);

					Transform (0.000000, 5.000000, 63.000000, 20.000000)
					{
						call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_OK'), CenterAlignedStyle (0, 'standard6.dif'));
					}

					Transform (1.000000, 1.000000, 61.000000, 18.000000)
					{
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuOk)), TypeEvent (0, 1));
						call CullEventAction (CallFunctionAction (Function (Sound/PlayMenuHighLight)), TypeEvent (0, 9));
					}
				}
			}
		}
	}

	Transform (0.000000, 0.000000, 800.000000, 600.000000)
	{
		if ($Load/LoadState$ == 6)
		{
			call VariablePicture ($Load/LoadPicture$, NULL, NULL);

			Transform (280.000000, 200.000000, 512.000000, 128.000000)
			{
				call Picture ('Menu/menu_addserver_512x128.tga');

				Transform (10.000000, 8.000000, 120.000000, 20.000000)
				{
					call Effect (Color (0.000000, 0.000000, 0.000000, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'CONFIRMATION_HEADING_INFO'), Style (Style/HeadingStyle, 'Trebuchet MS8.dif'));
				}

				Transform (6.000000, 50.000000, 266.000000, 40.000000)
				{
					call Effect (Color (0.773438, 0.753906, 0.230469, 1.000000));
					call Text (BfLocaleString (BfLocaleData (Locale/Locale, $Locale/Valid$), $Locale/Valid$, 'INFO_MESSAGE_LOADING'), BfCenterStyle (0, 'Trebuchet MS14.dif'));
				}
			}
		}
	}

	Transform (0.000000, 0.000000, 20.000000, 20.000000)
	{
		if (false)
		{
			call Picture ('');
			call CullEventAction (ActionList (Set ($FocusEffect/DebriefingAlpha$, 1.000000), Set ($FocusEffect/BGAlpha$, 1.000000), Set ($Load/LoadState$, 0.000000), Set ($FocusEffect/LeftPos$, 0.000000), Set ($FocusEffect/RightPos$, 
					0.000000), Set ($FocusEffect/Alpha$, 1.000000), Set ($FocusEffect/SplashScreenAlpha$, 1.000000), Set ($FocusEffect/ButtonAlpha$, 1.000000), Set ($FocusEffect/BgPicAlpha$, 1.000000)), ButtonEvent (0, 
					1, 1));
		}
	}
}

// Variable list:
	Variable ($AlliedTicket$, String32, '9999');
	Variable ($AlliedTicketFlagLoad$, String32, '');
	Variable ($AxisTicket$, String32, '321');
	Variable ($AxisTicketFlagLoad$, String32, '');
	Variable ($Briefing/BriefingPicture$, String32, '../../Bf1942/Levels/Tobruk/Menu/briefing.tga');
	Variable ($Briefing/BriefingText$, WString, 'American and Japanese fleets are once again preparing for a major showdown in the Pacific - this time near Midway Island. Within striking distance of either Hawaii or Japan, Midway is of obvious strategic importance. Fortunately for the US, American naval command has learned secret information regarding the Japanese attack plan. While Japan conducts diversionary attacks, the US knows that the bulk of the Japanese force is heading toward US-controlled Midway. \n\nIt\'s now a tense waiting game as the US fleet patrols the region, hoping to spot the Japanese force before it spots them. The winner at Midway will have a clear advantage in the war in the Pacific.   \n');
	Variable ($Briefing/EscapeToCancel$, WString, 'PRESS ESCAPE TO CANCEL');
	Variable ($Briefing/ObjectivesText$, WString, 'sdsd');
	Variable ($CampaignScore$, Int32, 20);
	Variable ($CampaignVictory$, Int32, 10);
	Variable ($Debriefing/DebriefingHeading$, WString, 'VICTORY');
	Variable ($Debriefing/DebriefingText$, WString, '');
	Variable ($Debriefing/ShowCampaignDebriefing$, Bool, true);
	Variable ($Debriefing/ShowHeading$, Bool, false);
	Variable ($FocusEffect/Abort$, Int32, 1);
	Variable ($FocusEffect/Alpha$, Float, 1.000000);
	Variable ($FocusEffect/BGAlpha$, Float, 1.000000);
	Variable ($FocusEffect/BgPicAlpha$, Float, 1.000000);
	Variable ($FocusEffect/ButtonAlpha$, Float, 1.000000);
	Variable ($FocusEffect/DebriefingAlpha$, Float, 1.000000);
	Variable ($FocusEffect/GoFadeIn$, Bool, false);
	Variable ($FocusEffect/GoFadeInButton$, Bool, false);
	Variable ($FocusEffect/GoFadeInLoadPicture$, Bool, false);
	Variable ($FocusEffect/GoFadeOut$, Bool, false);
	Variable ($FocusEffect/GoFadeOut1$, Bool, false);
	Variable ($FocusEffect/GoFadeOut2$, Bool, false);
	Variable ($FocusEffect/GoFadeOut3$, Bool, false);
	Variable ($FocusEffect/GoFadeOutLoadPicture$, Bool, false);
	Variable ($FocusEffect/GoMoveLeftIn$, Bool, false);
	Variable ($FocusEffect/GoMoveLeftOut$, Bool, false);
	Variable ($FocusEffect/GoMoveRightIn$, Bool, false);
	Variable ($FocusEffect/GoMoveRightOut$, Bool, false);
	Variable ($FocusEffect/GoMoveYIn$, Bool, false);
	Variable ($FocusEffect/GoMoveYOut$, Bool, false);
	Variable ($FocusEffect/GoPictureSwitch$, Bool, false);
	Variable ($FocusEffect/LeftPos$, Int32, 0);
	Variable ($FocusEffect/LoadAlpha$, Float, 1.000000);
	Variable ($FocusEffect/RightPos$, Int32, 0);
	Variable ($FocusEffect/SplashScreenAlpha$, Float, 1.000000);
	Variable ($FocusEffect/YPos$, Int32, 1);
	Variable ($Host/Create/GameType$, Int32, 3);
	Variable ($InfoMenu/InfoMenuComments1$, WString, '1');
	Variable ($InfoMenu/InfoMenuComments2$, WString, '2');
	Variable ($InfoMenu/InfoMenuComments3$, WString, '3');
	Variable ($InfoMenu/InfoMenuComments4$, WString, '4');
	Variable ($InfoMenu/InfoMenuComments5$, WString, '5');
	Variable ($InfoMenu/InfoMenuGameType$, WString, 'CAPTURE THE FLAG - ASSAULT MAP');
	Variable ($InfoMenu/InfoMenuGeneralInfo1$, WString, '50 ');
	Variable ($InfoMenu/InfoMenuGeneralInfo2$, WString, 'ON');
	Variable ($InfoMenu/InfoMenuGeneralInfo3$, WString, '100 ');
	Variable ($InfoMenu/InfoMenuHeading$, WString, 'TOBRUK');
	Variable ($InfoMenu/InfoMenuObjectives$, WString, 'MULTIPLAYER_BRIEFING_TOBRUK_OBJECTIVES,');
	Variable ($InhibitMenuBehavior$, Int32, 0);
	Variable ($Join/ShowFailedToJoin$, Int32, 0);
	Variable ($Load/LevelName$, WString, 'LOADING OMAHA BEACH');
	Variable ($Load/LoadPercent$, Float, 100.000000);
	Variable ($Load/LoadPicture$, String32, 'Load/Pacific.tga');
	Variable ($Load/LoadState$, Int32, 0);
	Variable ($Load/ShowDefaultLoadingPicture$, Bool, false);
	Variable ($Locale/Valid$, Bool, true);
	Variable ($MaxCampaignScore$, Float, 50.000000);
	Variable ($Password/NewPassword$, String32, '');
	Variable ($Password/ShowPassword$, Int32, 0);
	Variable ($ShowDebriefing$, Int32, 0);
	Variable ($StartingGame$, Int32, 2);
	Variable ($TransitionEffect$, Int32, 0);
