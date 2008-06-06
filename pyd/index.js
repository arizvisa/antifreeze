Ext.onReady(function() {

    /////////////////////////////////////////////////////////////////////////////////
    // GLOBALS
    /////////////////////////////////////////////////////////////////////////////////

    var codeStore;
    var coConstsString;
    var vanillaFieldSet;


    /////////////////////////////////////////////////////////////////////////////////
    // Navigation Tree
    /////////////////////////////////////////////////////////////////////////////////

    function treeStatusBeforeLoaded() {
        Ext.MessageBox.show({
            msg:            '<br><center>Loading PYD File...</center>',
            title:          'LOADING',
            width:          400,
            closable:       false
        });
    }

    function treeStatusLoaded() {
        Ext.MessageBox.hide();
    }


    var root_node = new Ext.tree.AsyncTreeNode({
        expanded:   true,
        text:       "PYD",
        border:     false
    });

    var tree = new Ext.tree.TreePanel({
        el:         'navArea',
        width:      900,
        height:     200,
        autoHeight: true,
        root:       root_node,
        loader:       new Ext.tree.TreeLoader({
            listeners:  {
                beforeload:     treeStatusBeforeLoaded,
                load:           treeStatusLoaded
                },
            dataUrl:    'json.py'
        })
    });

    // sort the tree
    var sortedTree = new Ext.tree.TreeSorter(tree, {});
    sortedTree.doSort(tree.getRootNode());

    // tree.expandAll();

    /////////////////////////////////////////////////////////////////////////////////
    // Dissassembly Window
    /////////////////////////////////////////////////////////////////////////////////
    
    var centerEditor = new Ext.form.TextArea({
        style:          'font-family: Courier'
    });


    var path     = "";
    var nodeName = "";

    function assembleCode() {
        var toAssemble = centerEditor.getValue();

        var xmlData = '<?xml version="1.0"?>';
        
        xmlData += '<code>';
        xmlData += '<name>' + nodeName + '</name>';
        xmlData += '<asm><![CDATA[' + toAssemble + ']]></asm>';
        xmlData += coConstsString;
        xmlData += '<path>' + path + '</path>';
        xmlData += '</code>';

        document.write('<!--' + xmlData + '-->');

        // need to send toAssemble to asm.py
        Ext.Ajax.request({
            url:    'asm.py',
            params: {
                'xmlData':    xmlData
            }
        });
    }


    var action = new Ext.Action({
        text:       'Assemble',
        handler:    assembleCode
    });

    var centerMenu = new Ext.Panel({
        height:         27,       // good height of menu item graphic is 27 (when there are no frames/borders)

        // ZOMG i hate this fucking javascript object notation crap
        tbar:   [{
                text:   'Edit',
                menu:   [action]
            }]
    });


    var centerPanel = new Ext.Panel({
        autoHeight: true,
        renderTo:   'center',
        //height:     201,  // 68 is the height of the (frame_borders + menu_graphics + rest_of_crap)
        items:      [centerMenu, centerEditor]
    });


    /////////////////////////////////////////////////////////////////////////////////
    // Code Object XML Data
    /////////////////////////////////////////////////////////////////////////////////
    
    var codeRecord = new Ext.data.Record.create([
        {name: 'name', mapping: 'name'},
        {name: 'asm'},
        {name: 'co_argcount'},
        {name: 'co_cellvars'},
        {name: 'co_code'},
        {name: 'co_consts'},
        {name: 'co_filename'},
        {name: 'co_firstlineno'},
        {name: 'co_flags'},
        {name: 'co_freevars'},
        {name: 'co_lnotab'},
        {name: 'co_name'},
        {name: 'co_names'},
        {name: 'co_nlocals'},
        {name: 'co_stacksize'},
        {name: 'co_varnames'}
    ]);

    var xmlReader = new Ext.data.XmlReader(
        {record: 'item',
         id:     'name'}, codeRecord);


    /////////////////////////////////////////////////////////////////////////////////
    // Code Properties
    /////////////////////////////////////////////////////////////////////////////////

    function saveProperties() {
        // figure out what combo item was chosen
        var selectedProp = codePropertiesCombo.getValue();

        // iterate over the items in the text fields, see what (if anything) has been changed
        var fieldItems = codePropertiesFieldSet.items;
        var itemValue = "";
        var origValue = "";

        if (selectedProp == "co_consts") {

            coConstsString = '<co_consts>';

            fieldItems.each(function(item, index, length) {
                if (item.isDirty()) {
                    itemValue = item.getValue();
                    origValue = item.initialConfig.emptyText;
                    
                    coConstsString += '<value index="' + index + '"><![CDATA[' + itemValue + ']]></value>';

                    //alert('Item ' + index + ' was changed from ' + origValue + ' to ' + itemValue);
                }
            });
            
            coConstsString += '</co_consts>';
        }


        

        // if not, we can just tell the user nothing has changed via a window msg
    }

    function revertProperties() {
        // figure out what combo item was chosen
        var selectedProp = codePropertiesCombo.getValue();
        
        // iterate over the items in the text fields, see what (if anything) has been changed
        var fieldItems = codePropertiesFieldSet.items;
        
        if (selectedProp == "co_consts") {
            
            fieldItems.each(function(item, index, length) {
                if (item.isDirty()) {
                    item.setValue(item.initialConfig.emptyText);
                }
            });
        }

    }

    var codePropertiesStore = new Ext.data.SimpleStore({
        fields: ['property'],
        data: [
        ['co_argcount'],
        ['co_cellvars'],
        ['co_code'],
        ['co_consts'],
        ['co_filename'],
        ['co_firstlineno'],
        ['co_flags'],
        ['co_freevars'],
        ['co_lnotab'],
        ['co_name'],
        ['co_names'],
        ['co_nlocals'],
        ['co_stacksize'],
        ['co_varnames']
        ]
    });


    var codePropertiesCombo = new Ext.form.ComboBox({
        store:          codePropertiesStore,
        fieldLabel:     'Property',
        displayField:   'property',
        typeAhead:      true,
        mode:           'local',
        width:          250,
        triggerAction:  'all',
        disabled:       true,
        editable:       false,
        emptyText:      'Select a property...'
    });

    vanillaFieldSet = new Ext.form.FieldSet({
        id:         'codePropsValues',
        title:      'Values',
        frame:      true,
        buttons:    [{
                text:       'Save',
                handler:    saveProperties
            },{
                text:       'Revert Values',
                handler:    revertProperties
            }]
    });


    var formPanel = new Ext.form.FormPanel({
        labelWidth:     70,
        frame:          true,
        //title:          'Code Properties Form',
        bodyStyle:      'padding:5px 5px 0',
        //autoWidth:      true,
        defaultType:    'textfield',
        items:          [codePropertiesCombo]
    });


    // gotta do dynamically
    var codePropertiesFieldSet = vanillaFieldSet.cloneConfig();
    formPanel.add(codePropertiesFieldSet);
    formPanel.doLayout();


    /////////////////////////////////////////////////////////////////////////////////
    // ViewPort
    /////////////////////////////////////////////////////////////////////////////////
    
    var viewport = new Ext.Viewport({
        layout:     'border',
        items: [{
                region:         'north',
                el:             'north',
                id:             'northRegion',
                title:          'AntiFreeze',
                height:         26,
                border:         false,
                split:          false
            },{
                region:         'west',
                el:             'west',
                id:             'westRegion',
                title:          'Navigation',
                split:          true,
                width:          450,        // REQUIRED! can only have 1 autoWidth in a given column of <div>s
                collapsible:    false,
                autoScroll:     true,
                items:          tree
            },{
                region:         'center',
                el:             'center',
                id:             'centerRegion',
                title:          'Disassembly Window',
                autoHeight:     true,       // if this is true, the size is set according to the size of the contents of items[]
                width:          800,
                split:          false,
                items:          centerPanel
            },{
                region:         'east',
                el:             'east',
                id:             'eastRegion',
                title:          'Code Properties',
                split:          true,
                width:          450,        // REQUIRED! must specify width
                collapsible:    false,
                items:          formPanel
            },{
                region:         'south',
                el:             'south',
                id:             'southRegion',
                title:          'Copyright 2008 Aaron Portnoy & Ali Rizvi-Santiago',
                split:          false,      // not resizable
                height:         15        // should not be autoHeight'd! that would fuck up lots of calculations
                //items:          codePropertiesTabs
            }]
    });


    // get the region heights, set the editor to a size based on that
    var westHeight = viewport.getComponent('westRegion').getEl().getHeight();
    var eastHeight = viewport.getComponent('eastRegion').getEl().getHeight();
    var northHeight = viewport.getComponent('northRegion').getEl().getHeight();
    var southHeight = viewport.getComponent('southRegion').getEl().getHeight();
    var totalHeight = westHeight + northHeight + southHeight;

    // - is the height of the (frame_borders + menu_graphics + rest_of_crap)
    centerEditor.setSize('100%', westHeight-53);
    formPanel.setSize('100%', westHeight-14);


    /////////////////////////////////////////////////////////////////////////////////
    // Event Listener for click on navigation tree
    /////////////////////////////////////////////////////////////////////////////////
    
    tree.on('click', function(node,e) {
        Ext.get(e.target).highlight();


        // get the name of the node that was clicked
        nodeName = node.text;

        // show load
        Ext.MessageBox.show({
            title:      'LOADING',
            closable:   false,
            width:      400,
            msg:    '<br><center>Loading ' + nodeName + '...</center>'
        });

        // find the entire path to the root node
        path = "->" + nodeName;
        var pNode = node.parentNode;

        while (pNode != null) {

            // look ahead to see if we're gonna hit the root node
            pParentNode = pNode.parentNode;

            if (pParentNode == null) {
                tmp = pNode.text + path;
            } else {
                tmp = "->" + pNode.text + path;
            }

            // update pNode for the while check
            pNode = pParentNode;

            path = tmp;
        }


        // instantiate store
        codeStore = new Ext.data.Store({
            proxy: new Ext.data.HttpProxy({
                url:    'disasm.py',
                method: 'post'
            }),
            baseParams: { codeName: nodeName, path: path },
            // XXX: add a success and failure listener
            reader: xmlReader
        });

        // this shit does NOT block!
        codeStore.load();
        
        
        /////////////////////////////////////////////////////////////////////////////////
        // Event listener for when store is done loading or on any subsequent access
        /////////////////////////////////////////////////////////////////////////////////
        
        codeStore.on('load', function() {

            // enable the code properties combobox
            codePropertiesCombo.enable();

            // remove the form field
            var formItems = formPanel.items

            // destroy the items
            formItems.each(function(item, index, length) {
                if (index != 0) {
                    item.destroy();
                }
            });

            // add the blank one back in
            codePropertiesFieldSet = vanillaFieldSet.cloneConfig();
            formPanel.add(codePropertiesFieldSet);

            // clear the combo box
            codePropertiesCombo.clearValue();

            // redraw form
            formPanel.doLayout();

            // update disassembly
            centerEditor.setValue(codeStore.getAt(0).get('asm'));

            Ext.MessageBox.hide();

        });

    // end tree 'on click'
    });


    /////////////////////////////////////////////////////////////////////////////////
    // event handler for code property combobox
    /////////////////////////////////////////////////////////////////////////////////
    
    codePropertiesCombo.on('select', function(combo, record, index) {

        // remove the old field set
        var formItems = formPanel.items;

        codePropertiesFieldSet = vanillaFieldSet.cloneConfig();
        formPanel.add(codePropertiesFieldSet);

        formItems.each(function(item, index, length) {
            if (index != 0) {
                item.destroy();
            }
        });

        // get the property name that was selected
        var propName = combo.getValue();

        if (propName == "co_consts") {

            // grab the xml data record we want
            var coConsts = codeStore.getAt(0).get('co_consts');

            var tokens = coConsts.split(",");

            // redraw
            formPanel.doLayout();

            var i = 0;
            for (i; i < tokens.length-1; i++) {

                var ident     = tokens[i].substr(0, 4);
                var tokenData = tokens[i].substring(4, tokens[i].length);

                // String
                if (ident == "STR:") {
                    codePropertiesFieldSet.add(new Ext.form.TextField({
                            fieldLabel: 'Index ' + i, 
                            emptyText:  tokenData, 
                            growMin:    200,
                            width:      200,
                            grow:       true
                        }));
                }

                // None
                else if (ident == "NON:") {
                    codePropertiesFieldSet.add(new Ext.form.TextField({
                            fieldLabel: 'Index ' + i,
                            width:      100,
                            disabled:   true,
                            emptyText:  'None'
                        }));
                }

                // Integer
                else if (ident == "INT:") {
                    codePropertiesFieldSet.add(new Ext.form.TextField({
                            fieldLabel: 'Index ' + i,
                            emptyText:  tokenData,
                            growMin:    200,
                            width:      200,
                            grow:       true
                        }));
                
                // else
                } else {
                    codePropertiesFieldSet.add(new Ext.form.TextField({
                            fieldLabel: 'Index ' + i,
                            emptyText:  tokenData,
                            disabled:   true,
                            width:      100,
                            grow:       true
                        }));
                }
            }


        // end co_consts
        } else if (propName == "co_argcount") {

            // grab the xml data record we want
            var coArgcount = codeStore.getAt(0).get('co_argcount');
            codePropertiesFieldSet.add(new Ext.form.TextField({
                fieldLabel: 'Arg Count',
                emptyText:  coArgcount,
                disabled:   true
                }));

        } else if (propName == "co_cellvars") {

            // grab the xml data record we want
            var coCellvars = codeStore.getAt(0).get('co_cellvars');
            codePropertiesFieldSet.add(new Ext.form.TextField({
                fieldLabel: 'Cell Vars',
                emptyText:  coCellvars,
                disabled:   true,
                grow:       true
                }));

        } else if (propName == "co_code") {

            // grab the xml data record we want
            var coCode = codeStore.getAt(0).get('co_code');

            codePropertiesFieldSet.add(new Ext.form.TextArea({fieldLabel: 'Bytecode', emptyText: coCode, disabled: true, grow: true, width: 250, height: 400}));

        } else if (propName == "co_filename") {

            // grab the xml data record we want
            var coFilename = codeStore.getAt(0).get('co_filename');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'Filename', emptyText: coFilename, disabled: true, grow: true}));
        } else if (propName == "co_firstlineno") {

            // grab the xml data record we want
            var coFirstlineno = codeStore.getAt(0).get('co_firstlineno');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'Firstlineno', emptyText: coFirstlineno, disabled: true, grow: true}));
        } else if (propName == "co_flags") {

            // grab the xml data record we want
            var coFlags = codeStore.getAt(0).get('co_flags');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'Flags', emptyText: coFlags, disabled: true}));
        } else if (propName == "co_freevars") {

            // grab the xml data record we want
            var coFreevars = codeStore.getAt(0).get('co_freevars');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'Freevars', emptyText: coFreevars, disabled: true, grow: true}));
        } else if (propName == "co_lnotab") {

            // grab the xml data record we want
            var coLnotab = codeStore.getAt(0).get('co_lnotab');

            codePropertiesFieldSet.add(new Ext.form.TextArea({fieldLabel: 'Lnotab', emptyText: coLnotab, disabled: true, grow: true, width: 250, height: 400}));
        } else if (propName == "co_name") {

            // grab the xml data record we want
            var coName = codeStore.getAt(0).get('co_name');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'Name', emptyText: coName, disabled: true, grow: true}));
        } else if (propName == "co_names") {

            // grab the xml data record we want
            var coNames = codeStore.getAt(0).get('co_names');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'Names', emptyText: coNames, disabled: true, grow: true}));
        } else if (propName == "co_nlocals") {

            // grab the xml data record we want
            var coNlocals = codeStore.getAt(0).get('co_nlocals');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'NLocals', emptyText: coNlocals, disabled: true, grow: true}));
        } else if (propName == "co_stacksize") {

            // grab the xml data record we want
            var coStacksize = codeStore.getAt(0).get('co_stacksize');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'Stacksize', emptyText: coStacksize, disabled: true, grow: true}));
        } else if (propName == "co_varnames") {

            // grab the xml data record we want
            var coVarnames = codeStore.getAt(0).get('co_varnames');

            codePropertiesFieldSet.add(new Ext.form.TextField({fieldLabel: 'Varnames', emptyText: coVarnames, disabled: true, grow: true}));
        }


        codePropertiesFieldSet.doLayout();
        formPanel.doLayout();

    });




// end onReady
});
