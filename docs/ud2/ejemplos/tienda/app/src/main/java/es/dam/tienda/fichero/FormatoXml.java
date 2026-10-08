package es.dam.tienda.fichero;

import java.io.IOException;
import java.io.InputStream;
import java.io.Writer;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

/** Documento XML con un elemento raíz catalogo y un elemento producto por producto. Usa DOM. */
public class FormatoXml implements FormatoProductos {

    @Override
    public List<ProductoDto> leer(Path ruta) throws IOException {
        try (InputStream entrada = Files.newInputStream(ruta)) {
            Document documento = nuevoConstructor().parse(entrada);   // todo el árbol en memoria
            NodeList nodos = documento.getElementsByTagName("producto");
            List<ProductoDto> productos = new ArrayList<>();
            for (int i = 0; i < nodos.getLength(); i++) {
                Element producto = (Element) nodos.item(i);
                productos.add(new ProductoDto(
                        producto.getAttribute("codigo"),
                        texto(producto, "nombre"),
                        new BigDecimal(texto(producto, "precio")),
                        Integer.parseInt(texto(producto, "stock"))));
            }
            return productos;
        } catch (ParserConfigurationException | SAXException | NumberFormatException e) {
            throw new IOException("XML no válido en " + ruta + ": " + e.getMessage(), e);
        }
    }

    @Override
    public void escribir(Path ruta, List<ProductoDto> productos) throws IOException {
        try {
            Document documento = nuevoConstructor().newDocument();
            Element catalogo = documento.createElement("catalogo");
            documento.appendChild(catalogo);
            for (ProductoDto p : productos) {
                Element producto = documento.createElement("producto");
                producto.setAttribute("codigo", p.codigo());
                hijo(documento, producto, "nombre", p.nombre());
                hijo(documento, producto, "precio", p.precio().toPlainString());
                hijo(documento, producto, "stock", String.valueOf(p.stock()));
                catalogo.appendChild(producto);
            }
            Transformer transformador = TransformerFactory.newInstance().newTransformer();
            transformador.setOutputProperty(OutputKeys.INDENT, "yes");
            transformador.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
            transformador.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
            try (Writer salida = Files.newBufferedWriter(ruta)) {                  // UTF-8
                salida.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");   // la cabecera, en su línea
                transformador.transform(new DOMSource(documento), new StreamResult(salida));
            }
        } catch (ParserConfigurationException | TransformerException e) {
            throw new IOException("No se pudo escribir " + ruta + ": " + e.getMessage(), e);
        }
    }

    private static DocumentBuilder nuevoConstructor() throws ParserConfigurationException {
        DocumentBuilderFactory fabrica = DocumentBuilderFactory.newInstance();
        // No procesar DTD: protege de ataques XXE si el fichero viene de fuera
        fabrica.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        DocumentBuilder constructor = fabrica.newDocumentBuilder();
        constructor.setErrorHandler(new DefaultHandler());   // los errores llegan como excepción, sin imprimirse
        return constructor;
    }

    private static void hijo(Document documento, Element padre, String etiqueta, String texto) {
        Element elemento = documento.createElement(etiqueta);
        elemento.setTextContent(texto);
        padre.appendChild(elemento);
    }

    private static String texto(Element padre, String etiqueta) throws IOException {
        NodeList encontrados = padre.getElementsByTagName(etiqueta);
        if (encontrados.getLength() == 0) {
            throw new IOException("Falta el elemento <" + etiqueta + "> en el producto "
                    + padre.getAttribute("codigo"));
        }
        return encontrados.item(0).getTextContent().strip();
    }
}
